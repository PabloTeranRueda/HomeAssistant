
import { Component, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  private http = inject(HttpClient);

  shoppingList = signal<string[]>([]);

  ngOnInit() {
    this.http
      .get<string[]>('http://127.0.0.1:8000/api/v1/shopping-list')
      .subscribe(items => {
        this.shoppingList.set(items);
      });
  }

  deleteItem(itemToDelete: string) {
    this.http.delete(
        `http://127.0.0.1:8000/api/v1/shopping-list?item=${encodeURIComponent(itemToDelete)}`
      ).subscribe(() => {
        this.shoppingList.update(items =>
          items.filter(item => item !== itemToDelete)
        );
      });
    }
}
