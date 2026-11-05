// Phase 10 - OCR - Text from image
// Tamil + English + Hindi text reading from photo / screenshot (user shared)
export interface IOCR {
  readText(photoPath: string): Promise<string>;
}
