import { CommonModule } from '@angular/common';
import { Component, input } from '@angular/core';

interface ComponentData {
  type: 'metrics' | 'chart' | 'table';
  title: string;
  data: any;
  styles?: { [key: string]: string };
}

@Component({
  selector: 'app-artifact-container',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './artifact-container.component.html',
  styleUrl: './artifact-container.component.css',
})
export class ArtifactContainerComponent {
  data = input<ComponentData | null>(null);
}
