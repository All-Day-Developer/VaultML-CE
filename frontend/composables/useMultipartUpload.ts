export interface UploadProgress {
  uploadedBytes: number
  totalBytes: number
  percentage: number
  currentPart: number
  totalParts: number
  speed: number // bytes per second
  remainingTime: number // seconds
}

export interface ChunkedUploadOptions {
  modelName: string
  filename: string
  file: File
  chunkSize?: number // defaults to 100MB
  onProgress?: (progress: UploadProgress) => void
  onError?: (error: Error) => void
  onComplete?: (result: any) => void
}

interface UploadChunk {
  chunkNumber: number
  size: number
}

export class ChunkedUploadManager {
  private version: number | null = null
  private chunks: UploadChunk[] = []
  private aborted = false
  private paused = false
  private startTime = 0
  
  constructor(private options: ChunkedUploadOptions) {}

  async start(): Promise<void> {
    this.aborted = false
    this.paused = false
    this.startTime = Date.now()
    
    try {
      // Initiate chunked upload
      const initResponse = await $fetch(`/api/models/${this.options.modelName}/versions/chunked/initiate`, {
        method: 'POST',
        body: {
          filename: this.options.filename,
          content_type: this.options.file.type || 'application/octet-stream'
        }
      })
      
      this.version = initResponse.version
      
      const chunkSize = this.options.chunkSize || 100 * 1024 * 1024 // 100MB default
      const totalChunks = Math.ceil(this.options.file.size / chunkSize)
      
      // Upload chunks sequentially or in parallel batches
      const concurrency = 3 // Upload 3 chunks at once
      const promises: Promise<void>[] = []
      
      for (let i = 0; i < totalChunks; i++) {
        const promise = this.uploadChunk(i + 1, chunkSize, totalChunks)
        promises.push(promise)
        
        // Limit concurrency
        if (promises.length >= concurrency) {
          await Promise.all(promises)
          promises.length = 0
        }
        
        if (this.aborted) break
      }
      
      // Wait for remaining chunks
      if (promises.length > 0) {
        await Promise.all(promises)
      }
      
      if (!this.aborted) {
        await this.complete()
      }
    } catch (error) {
      if (!this.aborted) {
        this.options.onError?.(error as Error)
        await this.abort()
      }
    }
  }
  
  private async uploadChunk(chunkNumber: number, chunkSize: number, totalChunks: number): Promise<void> {
    if (this.aborted) return
    
    const start = (chunkNumber - 1) * chunkSize
    const end = Math.min(start + chunkSize, this.options.file.size)
    const chunk = this.options.file.slice(start, end)
    
    try {
      // Upload the chunk to our Python API
      const formData = new FormData()
      formData.append('chunk', chunk, `chunk-${chunkNumber}`)
      
      const uploadResponse = await fetch(
        `/api/models/${this.options.modelName}/versions/${this.version}/chunks/${chunkNumber}`,
        {
          method: 'PUT',
          body: formData
        }
      )
      
      if (!uploadResponse.ok) {
        throw new Error(`Failed to upload chunk ${chunkNumber}: ${uploadResponse.statusText}`)
      }
      
      const result = await uploadResponse.json()
      
      // Store chunk info for tracking
      this.chunks.push({
        chunkNumber: chunkNumber,
        size: result.size
      })
      
      // Update progress
      this.updateProgress(chunkNumber, totalChunks)
      
    } catch (error) {
      console.error(`Failed to upload chunk ${chunkNumber}:`, error)
      throw error
    }
  }
  
  private updateProgress(completedChunk: number, totalChunks: number): void {
    const uploadedBytes = this.chunks.reduce((total, chunk) => total + chunk.size, 0)
    const totalBytes = this.options.file.size
    const percentage = Math.min((uploadedBytes / totalBytes) * 100, 100)
    
    const elapsed = (Date.now() - this.startTime) / 1000 // seconds
    const speed = uploadedBytes / elapsed
    const remainingBytes = totalBytes - uploadedBytes
    const remainingTime = remainingBytes / speed
    
    this.options.onProgress?.({
      uploadedBytes,
      totalBytes,
      percentage,
      currentPart: completedChunk,
      totalParts: totalChunks,
      speed,
      remainingTime: isFinite(remainingTime) ? remainingTime : 0
    })
  }
  
  private async complete(): Promise<void> {
    if (!this.version) {
      throw new Error('Upload not initiated')
    }
    
    // Complete the chunked upload (backend combines chunks and uploads to S3)
    const completeResponse = await $fetch(
      `/api/models/${this.options.modelName}/versions/${this.version}/chunked/complete`,
      {
        method: 'POST'
      }
    )
    
    this.options.onComplete?.(completeResponse)
  }
  
  async pause(): Promise<void> {
    this.paused = true
  }
  
  async resume(): Promise<void> {
    this.paused = false
  }
  
  async abort(): Promise<void> {
    this.aborted = true
    
    if (this.version) {
      try {
        await $fetch(
          `/api/models/${this.options.modelName}/versions/${this.version}/chunked/abort`,
          {
            method: 'DELETE'
          }
        )
      } catch (error) {
        console.error('Failed to abort chunked upload:', error)
      }
    }
  }
  
  get isAborted(): boolean {
    return this.aborted
  }
  
  get isPaused(): boolean {
    return this.paused
  }
}

export function useChunkedUpload() {
  const createUpload = (options: ChunkedUploadOptions) => {
    return new ChunkedUploadManager(options)
  }
  
  const formatFileSize = (bytes: number): string => {
    const units = ['B', 'KB', 'MB', 'GB', 'TB']
    let size = bytes
    let unitIndex = 0
    
    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024
      unitIndex++
    }
    
    return `${size.toFixed(1)} ${units[unitIndex]}`
  }
  
  const formatSpeed = (bytesPerSecond: number): string => {
    return `${formatFileSize(bytesPerSecond)}/s`
  }
  
  const formatTime = (seconds: number): string => {
    if (!isFinite(seconds)) return '--:--'
    
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = Math.floor(seconds % 60)
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`
  }
  
  return {
    createUpload,
    formatFileSize,
    formatSpeed,
    formatTime
  }
}