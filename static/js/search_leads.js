document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search');
  const leadRows = document.querySelectorAll('.lead-row');

  searchInput.addEventListener('input', () => {
      console.log('searching')
      const query = searchInput.value.toLowerCase();

      leadRows.forEach(row => {
          const cells = row.querySelectorAll('.lead-column');
          const rowText = Array.from(cells)
              .map(cell => cell.textContent.toLowerCase())
              .join(' ');

          if (rowText.includes(query)) {
              row.style.display = ''; // Show the row
          } else {
              row.style.display = 'none'; // Hide the row
          }
      });
  });
});
