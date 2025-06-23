import { afterNextRender, Component, ElementRef, inject } from '@angular/core';
import { createSwapy } from 'swapy';

@Component({
  selector: 'app-dnd-page',
  standalone: true,
  templateUrl: './dnd-page.component.html',
  styleUrl: './dnd-page.component.css',
})
export class DndPageComponent {
  el = inject(ElementRef);

  constructor() {
    afterNextRender({
      write: () => {
        const swapy = createSwapy(this.el.nativeElement, {
          animation: 'dynamic',
        });
      },
    });
  }

  removeOnClick(target: EventTarget | null) {
    if (target instanceof HTMLElement && target.parentNode) {
      console.log('removing');
      target.parentNode.removeChild(target);
    }
  }

  getCurrentLayout() {
    console.log(this.el.nativeElement);
  }
}
