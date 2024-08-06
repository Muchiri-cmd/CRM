document.getElementById('filter-toggle').addEventListener('click', function() {
  let filterSection = document.getElementById('filter-section');
  if (filterSection.style.display === 'none' || filterSection.style.display === '') {
    filterSection.style.display = 'block';
  } else {
    filterSection.style.display = 'none';
  }
});

// Initialize price range slider values
const priceMinRange = document.getElementById('price-min');
const priceMaxRange = document.getElementById('price-max');
const priceMinValue = document.getElementById('price-min-value');
const priceMaxValue = document.getElementById('price-max-value');

// Sync price range slider values with display
function updatePriceValues() {
  priceMinValue.textContent = priceMinRange.value;
  priceMaxValue.textContent = priceMaxRange.value;
}

priceMinRange.addEventListener('input', updatePriceValues);
priceMaxRange.addEventListener('input', updatePriceValues);

// Initialize project size slider values
const sizeMinRange = document.getElementById('size-min');
const sizeMaxRange = document.getElementById('size-max');
const sizeMinValue = document.getElementById('size-min-value');
const sizeMaxValue = document.getElementById('size-max-value');

// Sync project size slider values with display
function updateSizeValues() {
  sizeMinValue.textContent = sizeMinRange.value;
  sizeMaxValue.textContent = sizeMaxRange.value;
}

sizeMinRange.addEventListener('input', updateSizeValues);
sizeMaxRange.addEventListener('input', updateSizeValues);

// Reset filters
document.getElementById('clear-filters').addEventListener('click', function() {
  document.getElementById('filter-form').reset();
  updatePriceValues(); // Reset price slider values display
  updateSizeValues(); // Reset size slider values display
  window.location.href = window.location.pathname;
});

// Initialize slider values display
updatePriceValues();
updateSizeValues();
