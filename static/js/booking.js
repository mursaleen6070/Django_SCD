document.addEventListener("DOMContentLoaded", () => {
    const ratesScript = document.getElementById("room-rates-data");
    const summaryCard = document.getElementById("bookingSummary");
    if (!ratesScript || !summaryCard) {
        return;
    }

    const rateMap = JSON.parse(ratesScript.textContent || "{}");
    const airportCharge = Number(summaryCard.dataset.airportCharge || 0);

    const roomTypeField = document.getElementById("id_room_type");
    const daysField = document.getElementById("id_booking_days");
    const airportField = document.getElementById("id_airport_pick_drop");

    const summaryRoomType = document.getElementById("summaryRoomType");
    const summaryDays = document.getElementById("summaryDays");
    const summaryRoomRent = document.getElementById("summaryRoomRent");
    const summaryAirport = document.getElementById("summaryAirport");
    const summaryTotal = document.getElementById("summaryTotal");

    const currencyFormatter = new Intl.NumberFormat("en-PK");

    const formatCurrency = (value) => `Rs. ${currencyFormatter.format(value)}`;

    function calculateTotal() {
        const roomType = roomTypeField ? roomTypeField.value : null;
        const nightlyRate = rateMap[roomType] || 0;
        let days = Number(daysField?.value || 1);
        if (Number.isNaN(days)) {
            days = 1;
        }
        days = Math.min(Math.max(days, 1), 7);
        if (daysField) {
            daysField.value = days;
        }
        const includeAirport = airportField?.checked;

        const baseRent = nightlyRate * days;
        const airportFee = includeAirport ? airportCharge : 0;
        const total = baseRent + airportFee;

        if (summaryRoomType) {
            const selectedOption = roomTypeField?.options[roomTypeField.selectedIndex];
            summaryRoomType.textContent = selectedOption ? selectedOption.text : "—";
        }
        if (summaryDays) {
            summaryDays.textContent = days === 1 ? "1 night" : `${days} nights`;
        }
        if (summaryRoomRent) {
            summaryRoomRent.textContent = formatCurrency(baseRent);
        }
        if (summaryAirport) {
            summaryAirport.textContent = formatCurrency(airportFee);
        }
        if (summaryTotal) {
            summaryTotal.textContent = formatCurrency(total);
        }
    }

    [roomTypeField, daysField, airportField].forEach((field) => {
        if (!field) return;
        const eventName = field.type === "checkbox" ? "change" : "input";
        field.addEventListener(eventName, calculateTotal);
    });

    calculateTotal();
});
