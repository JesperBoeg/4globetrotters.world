/*
Email signup widget JavaScript.
Handles JSON submissions to Formspree or any webhook endpoint.
*/

(function() {
  'use strict';

  // Initialize signup forms
  function initEmailSignupForms() {
    const forms = document.querySelectorAll('.email-signup-form');
    
    forms.forEach(form => {
      form.addEventListener('submit', handleSignupSubmit);
    });
  }

  // Handle form submission
  async function handleSignupSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const emailInput = form.querySelector('input[type="email"]');
    const button = form.querySelector('button');
    const successMessage = form.parentElement.querySelector('.signup-success');
    
    if (!emailInput || !emailInput.value) {
      alert('Please enter your email address');
      return;
    }

    // Disable button
    button.disabled = true;
    const originalText = button.textContent;
    button.textContent = 'Subscribing...';

    try {
      // Endpoint can be set on the form or parent widget.
      const endpoint =
        form.getAttribute('data-endpoint') ||
        (form.parentElement && form.parentElement.getAttribute('data-endpoint')) ||
        '';
      if (!endpoint) {
        throw new Error('Missing newsletter endpoint');
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: emailInput.value.trim()
        })
      });

      if (response.ok) {
        // Show success message
        emailInput.value = '';
        button.textContent = 'Subscribed!';
        if (successMessage) {
          successMessage.classList.add('show');
          setTimeout(() => {
            successMessage.classList.remove('show');
          }, 3000);
        }
      } else {
        throw new Error('Subscription failed. Please try again in a moment.');
      }
    } catch (error) {
      alert('Sorry, we could not subscribe you right now. Please try again in a moment.');
      console.error('Signup error:', error);
    } finally {
      // Re-enable button
      button.disabled = false;
      button.textContent = originalText;
    }
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEmailSignupForms);
  } else {
    initEmailSignupForms();
  }
})();
