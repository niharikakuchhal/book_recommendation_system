// books/static/js/scripts.js

$(document).ready(function() {
    // Search form submission
    $('#search-form').submit(function(e) {
        e.preventDefault();
        const query = $('#search-query').val();
        const searchType = $('#search-type').val();
        if (query.trim() !== '') {
            searchBooks(query, searchType);
        }
    });

    // Search books function
    function searchBooks(query, searchType) {
        axios.get('/search/', {
            params: {
                q: query,
                type: searchType
            }
        })
        .then(response => {
            const books = response.data;
            displaySearchResults(books);
        })
        .catch(error => {
            console.error('Error fetching search results:', error);
        });
    }

    // Display search results function
    function displaySearchResults(books) {
        const searchResultsContainer = $('#search-results');
        searchResultsContainer.empty();

        if (books.length > 0) {
            books.forEach(book => {
                const bookCard = `
                    <div class="book-card">
                        <div class="book-cover" style="background-image: url(${book.cover_url || ''});"></div>
                        <div class="book-details">
                            <h5>${book.title}</h5>
                            <p><strong>Author:</strong> ${book.author}</p>
                            <p>${book.description}</p>
                        </div>
                    </div>
                `;
                searchResultsContainer.append(bookCard);
            });
        } else {
            searchResultsContainer.append('<p>No books found.</p>');
        }
    }
    function getCSRFToken() {
        const name = 'csrftoken';
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Recommend form submission
    $('#recommend-form').submit(function(e) {
        e.preventDefault();
        const title = $('#book-title').val();
        const author = $('#book-author').val();
        const description = $('#book-description').val();
        const coverUrl = $('#book-cover-url').val();

        axios.post('/recommended_book/', {
            title,
            author,
            description,
            cover_url: coverUrl
        },{
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => {
            alert('Book recommended successfully!');
            $('#recommend-form')[0].reset();
        })
        .catch(error => {
            console.error('Error recommending book:', error);
        });
    });
});
