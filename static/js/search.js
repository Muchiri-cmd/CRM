document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search');
    const tableRows = document.querySelectorAll('.sales-pipeline-table tbody tr');

    searchInput.addEventListener('keyup', function () {
        const searchText = searchInput.value.toLowerCase();

        tableRows.forEach(function (row) {
            const cells = row.querySelectorAll('td');
            let rowText = '';

            cells.forEach(function (cell) {
                rowText += cell.textContent.toLowerCase();
            });

            if (rowText.includes(searchText)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});
