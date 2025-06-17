import { Component, Renderer2 } from '@angular/core';
import { ArtifactContainerComponent } from '../components/artifact-container/artifact-container.component';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { IframeLoaderComponent } from "../components/iframe-loader/iframe-loader.component";

interface ComponentData {
  type: 'metrics' | 'chart' | 'table';
  title: string;
  data: any;
  styles?: { [key: string]: string };
}

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.component.html',
  imports: [ArtifactContainerComponent, IframeLoaderComponent],
})
export class AppComponent {
  constructor(private renderer: Renderer2, private sanitizer: DomSanitizer) {}

  // 1. Solution
  responseCode = `<div class="metrics-container">
    <h1>NovaTech Metrics</h1>
    <p class="metrics-revenue">Revenue: 3.5$</p>
    <p class="metrics-market">
      Market cap: <span class="metrics-metric-percent">-3.2</span>
    </p>
  </div>`;

  handleClick() {
    const artifact = document.getElementById('artifact');

    if (artifact) {
      artifact.innerHTML = '';
      artifact.innerHTML = this.responseCode;
    }
  }

  // 2. Solution
  handleClickR() {
    const artifact = document.getElementById('artifact');

    if (artifact) {
      artifact.innerHTML = '';

      const container = this.renderer.createElement('div');
      this.renderer.addClass(container, 'metrics-container');

      const h1 = document.createElement('h1');
      const h1Text = this.renderer.createText('NovaTech Metrics');
      this.renderer.appendChild(h1, h1Text);
      this.renderer.appendChild(container, h1);

      const revenuePara = this.renderer.createElement('p');
      this.renderer.addClass(revenuePara, 'metrics-revenue');
      const revenueText = this.renderer.createText('Revenue: 3.5$');
      this.renderer.appendChild(revenuePara, revenueText);
      this.renderer.appendChild(container, revenuePara);

      const marketPara = this.renderer.createElement('p');
      this.renderer.addClass(marketPara, 'metrics-market');

      const marketText1 = this.renderer.createText('Market cap: ');
      this.renderer.appendChild(marketPara, marketText1);

      const percentSpan = this.renderer.createElement('span');
      this.renderer.addClass(percentSpan, 'metrics-metric-percent');
      const percentText = this.renderer.createText('-3.2');
      this.renderer.appendChild(percentSpan, percentText);
      this.renderer.appendChild(marketPara, percentSpan);

      this.renderer.appendChild(container, marketPara);

      // Final append
      this.renderer.appendChild(artifact, container);
    }
  }

  // 3. Solution - Template-based
  dynamicComponentData: ComponentData | null = null;

  backendResponse: ComponentData = {
    type: 'metrics',
    title: 'NovaTech Metrics',
    data: {
      revenue: '3.5$',
      marketCap: '-3.2',
    },
    styles: {
      backgroundColor: 'rgb(83, 83, 175)',
      color: 'white',
      padding: '8px',
      borderRadius: '12px',
    },
  };

  handleDynamicLoad() {
    this.dynamicComponentData = this.backendResponse;
  }
}
