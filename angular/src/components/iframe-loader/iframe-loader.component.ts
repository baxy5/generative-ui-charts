import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-iframe-loader',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="iframe-container">
      <button (click)="loadGeneratedComponent()">
        Load Generated Component
      </button>
      <button (click)="clearComponent()">Clear</button>
      <a [href]="iframeTestUrl" target="_blank"> <button>Open app</button></a>

      <iframe
        *ngIf="iframeTestUrl"
        [src]="iframeTestUrl"
        title="Generated Component"
        sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox allow-forms"
        width="100%"
        [style.height.px]="iframeHeight"
        loading="eager"
        style="color-scheme: normal; border: none;"
        (load)="onIframeLoad()"
      >
      </iframe>
    </div>
  `,
  styles: [
    `
      .iframe-container {
        width: 100%;
        margin: 20px 0;
      }

      iframe {
        border: 1px solid #ddd;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }
    `,
  ],
})
export class IframeLoaderComponent {
  currentUrl: SafeResourceUrl | null = null;
  iframeHeight = 600;

  iframeTestUrl: SafeResourceUrl;

  constructor(private sanitizer: DomSanitizer) {
    this.iframeTestUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
      'https://pub-b348006f0b2142f7a105983d74576412.r2.dev/4c8dd9016315/index.html'
    );
  }

  async loadGeneratedComponent() {
    // 1. Call backend agent to generate component
    // 2. Upload to your file storage (s3, ...)
    // 3. Load in iframe
  }

  private async callBackendAgent(): Promise<string> {
    return '';
  }

  private async uploadAndHost(htmlContent: string): Promise<string> {
    return '';
  }

  clearComponent() {
    this.currentUrl = null;
  }

  onIframeLoad() {
    // Optional: Auto-resize iframe based on content
    // This requires postMessage communication with the iframe content
  }
}
