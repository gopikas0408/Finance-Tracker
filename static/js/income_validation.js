document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("incomeForm");

    const incomeSource = document.getElementById("id_income_source");
    const amount = document.getElementById("id_amount");
    const paymentMode = document.getElementById("id_payment_mode");
    const receivedDate = document.getElementById("id_received_date");
    const description = document.getElementById("id_description");
    const attachment = document.getElementById("id_attachment");

    // Error Labels
    const incomeSourceError = document.getElementById("income_source_error");
    const amountError = document.getElementById("amount_error");
    const paymentModeError = document.getElementById("payment_mode_error");
    const receivedDateError = document.getElementById("received_date_error");
    const descriptionError = document.getElementById("description_error");
    const attachmentError = document.getElementById("attachment_error");


    function setError(input, errorElement, message) {

        input.classList.remove("is-valid");
        input.classList.add("is-invalid");

        errorElement.innerText = message;

    }

    function setSuccess(input, errorElement) {

        input.classList.remove("is-invalid");
        input.classList.add("is-valid");

        errorElement.innerText = "";

    }


    // ===========================
    // Income Source
    // ===========================

    function validateIncomeSource() {

        if (incomeSource.value === "") {

            setError(
                incomeSource,
                incomeSourceError,
                "Please select Income Source."
            );

            return false;

        }

        setSuccess(
            incomeSource,
            incomeSourceError
        );

        return true;

    }


    // ===========================
    // Amount
    // ===========================

    function validateAmount() {

        const value = amount.value.trim();

        if (value === "") {

            setError(
                amount,
                amountError,
                "Amount is required."
            );

            return false;

        }

        if (isNaN(value)) {

            setError(
                amount,
                amountError,
                "Amount must be numeric."
            );

            return false;

        }

        if (parseFloat(value) <= 0) {

            setError(
                amount,
                amountError,
                "Amount must be greater than 0."
            );

            return false;

        }

        if (parseFloat(value) > 999999999) {

            setError(
                amount,
                amountError,
                "Amount is too large."
            );

            return false;

        }

        setSuccess(
            amount,
            amountError
        );

        return true;

    }


    // ===========================
    // Payment Mode
    // ===========================

    function validatePaymentMode() {

        if (paymentMode.value === "") {

            setError(
                paymentMode,
                paymentModeError,
                "Please select Payment Mode."
            );

            return false;

        }

        setSuccess(
            paymentMode,
            paymentModeError
        );

        return true;

    }


    // ===========================
    // Received Date
    // ===========================

    function validateDate() {

        if (receivedDate.value === "") {

            setError(
                receivedDate,
                receivedDateError,
                "Received Date is required."
            );

            return false;

        }

        const selected = new Date(receivedDate.value);
        const today = new Date();

        today.setHours(0,0,0,0);

        if (selected > today) {

            setError(
                receivedDate,
                receivedDateError,
                "Future date is not allowed."
            );

            return false;

        }

        setSuccess(
            receivedDate,
            receivedDateError
        );

        return true;

    }


    // ===========================
    // Description
    // ===========================

    function validateDescription() {

        const value = description.value.trim();

        if (value !== "" && value.length < 5) {

            setError(
                description,
                descriptionError,
                "Minimum 5 characters."
            );

            return false;

        }

        if (value.length > 500) {

            setError(
                description,
                descriptionError,
                "Maximum 500 characters allowed."
            );

            return false;

        }

        setSuccess(
            description,
            descriptionError
        );

        return true;

    }


    // ===========================
    // Attachment
    // ===========================

    function validateAttachment() {

        if (attachment.files.length === 0) {

            attachmentError.innerText = "";
            attachment.classList.remove("is-invalid");
            attachment.classList.remove("is-valid");

            return true;

        }

        const file = attachment.files[0];

        const allowed = [
            "pdf",
            "jpg",
            "jpeg",
            "png"
        ];

        const extension = file.name.split(".").pop().toLowerCase();

        if (!allowed.includes(extension)) {

            setError(
                attachment,
                attachmentError,
                "Only PDF, JPG, JPEG, PNG files allowed."
            );

            return false;

        }

        if (file.size > 5 * 1024 * 1024) {

            setError(
                attachment,
                attachmentError,
                "Maximum file size is 5MB."
            );

            return false;

        }

        setSuccess(
            attachment,
            attachmentError
        );

        return true;

    }


    // ===========================
    // Live Validation
    // ===========================

    incomeSource.addEventListener("change", validateIncomeSource);

    amount.addEventListener("input", validateAmount);

    paymentMode.addEventListener("change", validatePaymentMode);

    receivedDate.addEventListener("change", validateDate);

    description.addEventListener("input", validateDescription);

    attachment.addEventListener("change", validateAttachment);


    // ===========================
    // Submit Validation
    // ===========================

    form.addEventListener("submit", function (e) {

        const valid =

            validateIncomeSource() &&
            validateAmount() &&
            validatePaymentMode() &&
            validateDate() &&
            validateDescription() &&
            validateAttachment();

        if (!valid) {

            e.preventDefault();

        }

    });

});