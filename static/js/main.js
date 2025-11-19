// ===========================
// 🔥 إعداد API BASE تلقائياً
// ===========================
const API_BASE = window.location.origin;

// متغيرات عامة
let selectedSeats = [];
let seatsData = {};

// تهيئة الصفحة
document.addEventListener("DOMContentLoaded", () => {
    loadSeats();
    setupEventListeners();
});

// ===========================
// 📌 تحميل بيانات المقاعد
// ===========================
async function loadSeats() {
    try {
        const response = await fetch(`${API_BASE}/api/seats`);
        if (!response.ok) throw new Error("API NOT FOUND");

        const data = await response.json();
        seatsData = data.seats || [];

        renderSeats();
    } catch (error) {
        console.error("خطأ في تحميل المقاعد:", error);
        showAlert("حدث خطأ في تحميل بيانات المقاعد", "error");
    }
}

// ===========================
// 📌 عرض المقاعد
// ===========================
function renderSeats() {
    const leftSection = document.getElementById("left-section");
    const rightSection = document.getElementById("right-section");

    const leftSeats = seatsData.filter(s => s.side === "left")
        .sort((a, b) => a.row_number - b.row_number);

    const rightSeats = seatsData.filter(s => s.side === "right")
        .sort((a, b) => a.row_number - b.row_number);

    renderSection(leftSection, leftSeats, "يسار");
    renderSection(rightSection, rightSeats, "يمين");
}

// ===========================
// 📌 عرض قسم مقاعد
// ===========================
function renderSection(sectionElement, seats, sectionName) {
    sectionElement.innerHTML = "";

    const title = document.createElement("div");
    title.className = "section-title";
    title.textContent = `الجانب ${sectionName}`;
    sectionElement.appendChild(title);

    const rows = {};
    seats.forEach(seat => {
        if (!rows[seat.row_number]) rows[seat.row_number] = [];
        rows[seat.row_number].push(seat);
    });

    Object.keys(rows).sort().forEach(rowNum => {
        const rowDiv = document.createElement("div");
        rowDiv.className = "row";

        const rowLabel = document.createElement("div");
        rowLabel.className = "row-label";
        rowLabel.textContent = `صف ${rowNum}`;
        rowDiv.appendChild(rowLabel);

        rows[rowNum].forEach(seat => {
            rowDiv.appendChild(createSeatElement(seat));
        });

        sectionElement.appendChild(rowDiv);
    });
}

// ===========================
// 📌 عنصر مقعد
// ===========================
function createSeatElement(seat) {
    const seatDiv = document.createElement("div");
    seatDiv.className = `seat ${seat.status}`;
    if (seat.category === "vip") seatDiv.classList.add("vip");

    seatDiv.textContent = seat.seat_number;
    seatDiv.dataset.seatId = seat.id;

    if (seat.status === "available") {
        seatDiv.addEventListener("click", () => toggleSeatSelection(seat));
    }

    return seatDiv;
}

// ===========================
// 📌 اختيار المقاعد
// ===========================
function toggleSeatSelection(seat) {
    selectedSeats = [seat];

    document.querySelectorAll(".seat").forEach(s =>
        s.classList.remove("selected")
    );

    document.querySelector(`[data-seat-id="${seat.id}"]`)
        ?.classList.add("selected");

    updateBookingForm();
}

// ===========================
// 📌 تحديث نموذج الحجز
// ===========================
function updateBookingForm() {
    const form = document.getElementById("booking-form");
    const info = document.getElementById("selected-seats");

    if (selectedSeats.length === 0) return form.style.display = "none";

    const s = selectedSeats[0];
    info.innerHTML = `
        <strong>المقعد المختار:</strong>
        ${s.side === "left" ? "يسار" : "يمين"} - صف ${s.row_number} - مقعد ${s.seat_number}
    `;

    form.style.display = "block";
}

// ===========================
// 📌 إرسال الحجز
// ===========================
async function handleBooking(event) {
    event.preventDefault();

    const name = document.getElementById("customer-name").value;
    const phone = document.getElementById("customer-phone").value;

    if (!name || !phone) return showAlert("يرجى ملء جميع الحقول", "error");

    const seatId = selectedSeats[0].id;

    try {
        const response = await fetch(`${API_BASE}/api/book-seat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ seat_id: seatId, customer_name: name, customer_phone: phone })
        });

        const data = await response.json();

        if (!data.success) return showAlert(data.message, "error");

        showAlert("تم إرسال طلب الحجز بنجاح!", "success");
        loadSeats();
    } catch {
        showAlert("حدث خطأ أثناء إرسال الحجز", "error");
    }
}

// ===========================
// 📌 Alerts
// ===========================
function showAlert(message, type) {
    const div = document.createElement("div");
    div.className = `alert alert-${type}`;
    div.textContent = message;

    document.querySelector(".container").prepend(div);
    setTimeout(() => div.remove(), 4000);
}

// ===========================
function setupEventListeners() {
    document.getElementById("booking-form-element")
        .addEventListener("submit", handleBooking);
}
