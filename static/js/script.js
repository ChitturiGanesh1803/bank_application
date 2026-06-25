document.addEventListener("DOMContentLoaded", function () {
  const accountForm = document.querySelector("#createAccountForm");
  const depositForm = document.querySelector("#depositForm");
  const withdrawForm = document.querySelector("#withdrawForm");

  if (accountForm) {
    accountForm.addEventListener("submit", function (event) {
      const phone = accountForm.querySelector("#phone_number");
      const phoneValue = phone.value.trim();
      if (!/^\d{10}$/.test(phoneValue)) {
        event.preventDefault();
        alert("Please enter a valid 10-digit phone number.");
      }
    });
  }

  if (depositForm) {
    depositForm.addEventListener("submit", function (event) {
      const accountNo = depositForm.querySelector("#account_no").value.trim();
      const amountValue = parseFloat(depositForm.querySelector("#amount").value);
      if (accountNo.length !== 10 || isNaN(amountValue) || amountValue <= 0) {
        event.preventDefault();
        alert("Please enter a valid account number and deposit amount.");
        return;
      }
      if (!confirm("Confirm deposit to account " + accountNo + "?")) {
        event.preventDefault();
      }
    });
  }

  if (withdrawForm) {
    withdrawForm.addEventListener("submit", function (event) {
      const accountNo = withdrawForm.querySelector("#account_no").value.trim();
      const amountValue = parseFloat(withdrawForm.querySelector("#amount").value);
      if (accountNo.length !== 10 || isNaN(amountValue) || amountValue <= 0) {
        event.preventDefault();
        alert("Please enter a valid account number and withdrawal amount.");
        return;
      }
      if (!confirm("Confirm withdrawal from account " + accountNo + "?")) {
        event.preventDefault();
      }
    });
  }
});
