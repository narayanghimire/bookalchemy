$(document).ready(function() {
    function showAlert(message, type) {
        var alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
        var alertHtml = '<div class="alert ' + alertClass + ' alert-dismissible fade show" role="alert">' +
                        message +
                        '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                        '<span aria-hidden="true">&times;</span>' +
                        '</button>' +
                        '</div>';
        $('#alert-container').html(alertHtml);
    }

    function showSuccessMessage(message) {
        $('#successMessage').text(message);
        $('#successModal').modal('show');
    }

    $('.delete-book').click(function() {
        var bookId = $(this).data('book-id');
        var bookElement = $('#book-' + bookId);

        $.ajax({
            url: window.location.protocol + '//' + window.location.host + '/books/' + bookId + '/delete',
            type: 'POST',
            success: function(response) {
                bookElement.remove();
                showAlert('Book successfully deleted!', 'success');
            },
            error: function(error) {
                showAlert('An error occurred while deleting the book.', 'error');
            }
        });
    });

    $('#addBookForm').submit(function(e) {
        e.preventDefault();

        var formData = $(this).serialize();

        $.ajax({
            url: window.location.protocol + '//' + window.location.host +'/books/add',
            type: 'POST',
            data: formData,
            success: function(response) {
                if (response.status === 'success') {
                    $('#addBookModal').modal('hide');
                    showSuccessMessage('Book successfully added!');

                    $('#reloadButton').click(function() {
                        location.reload();
                    });
                } else {
                    showSuccessMessage('An error occurred while adding the book.');
                }
            },
            error: function(error) {
                showSuccessMessage('An error occurred while adding the book.');
            }
        });
    });

    $('#addAuthorForm').submit(function(e) {
        e.preventDefault();

        var formData = $(this).serialize();

        $.ajax({
            url: window.location.protocol + '//' + window.location.host +'/authors/add',
            type: 'POST',
            data: formData,
            success: function(response) {
                if (response.status === 'success') {
                    $('#addAuthorModal').modal('hide');
                    showSuccessMessage('Author successfully added!');

                    $('#reloadButton').click(function() {
                        location.reload();
                    });
                } else {
                    showSuccessMessage('An error occurred while adding the author.');
                }
            },
            error: function() {
                showSuccessMessage('An error occurred while adding the author.');
            }
        });
    });

    $('#addBookModal').on('show.bs.modal', function() {
        $.ajax({
            url: window.location.protocol + '//' + window.location.host +'/authors',
            type: 'GET',
            success: function(response) {
                var authorsDropdown = $('#author_id');
                authorsDropdown.empty();
                authorsDropdown.append('<option disabled selected>Select Author</option>');
                response.authors.forEach(function(author) {
                    authorsDropdown.append('<option value="' + author.id + '">' + author.name + '</option>');
                });
            },
            error: function() {
                showAlert('Error loading authors', 'error');
            }
        });
    });
});
