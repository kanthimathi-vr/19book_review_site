from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

books = [
    {'id': 1, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'cover': 'covers/book1.jpg'},
    {'id': 2, 'title': '1984', 'author': 'George Orwell', 'cover': 'covers/book2.jpg'},
]

reviews = {
    1: [],
    2: [],
}

@app.route('/')
def list_books():
    return render_template('books.html', books=books)

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return "Book not found", 404

    if request.method == 'POST':
        username = request.form.get('username')
        rating = request.form.get('rating')
        text = request.form.get('review')
        if username and rating and text:
            review = {'username': username, 'rating': int(rating), 'text': text}
            reviews.setdefault(book_id, []).append(review)
            return redirect(url_for('book_detail', book_id=book_id))

    filter_rating = request.args.get('rating', type=int)
    book_reviews = reviews.get(book_id, [])
    filtered_reviews = [r for r in book_reviews if (filter_rating is None or r['rating'] == filter_rating)]

    return render_template('book_detail.html', book=book, reviews=filtered_reviews, filter_rating=filter_rating)

if __name__ == '__main__':
    app.run(debug=True)
