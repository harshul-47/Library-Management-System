from django.shortcuts import render
from .models import Book, Student, IssueBook


def home(request):
    return render(request, 'library/home.html')


def book_list(request):
    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    return render(request, 'library/books.html', {'books': books})


def add_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')

        if title and author and isbn:
            Book.objects.create(
                title=title,
                author=author,
                isbn=isbn
            )

    return render(request, 'library/add_book.html')


def issue_book(request):
    students = Student.objects.all()
    books = Book.objects.filter(available=True)

    if request.method == "POST":
        student_id = request.POST.get('student')
        book_id = request.POST.get('book')

        if student_id and book_id:
            student = Student.objects.get(id=student_id)
            book = Book.objects.get(id=book_id)

            IssueBook.objects.create(student=student, book=book)

            book.available = False
            book.save()

    return render(request, 'library/issue_book.html', {
        'students': students,
        'books': books
    })
