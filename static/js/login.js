document.addEventListener('DOMContentLoaded', function() {
  const passwordField = document.getElementById('password');
  const showPasswordToggle = document.getElementById('togglePassword');

  showPasswordToggle.addEventListener('click', function() {
    if (passwordField.type === 'password') {
      passwordField.type = 'text';
      showPasswordToggle.textContent = 'Hide';
    }
    else {
      passwordField.type = 'password';
      showPasswordToggle.textContent = 'Show';
    }
      
  });
});
