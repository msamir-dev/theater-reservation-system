// متغيرات عامة
let selectedSeats = [];
let seatsData = {};

// تهيئة الصفحة
document.addEventListener('DOMContentLoaded', function() {
    loadSeats();
    setupEventListeners();
});

// تحميل بيانات المقاعد
async function loadSeats() {
    try {
        const response = await fetch('/api/seats');
        const data = await response.json();
        // API returns {seats: [...]} so we need to extract the seats array
        seatsData = data.seats || data;
        renderSeats();
    } catch (error) {
        console.error('خطأ في تحميل المقاعد:', error);
        showAlert('حدث خطأ في تحميل بيانات المقاعد', 'error');
    }
}

// عرض المقاعد
function renderSeats() {
    const leftSection = document.getElementById('left-section');
    const rightSection = document.getElementById('right-section');
    
    // ترتيب المقاعد حسب الصفوف
    const leftSeats = seatsData.filter(seat => seat.side === 'left')
        .sort((a, b) => a.row_number - b.row_number || a.seat_number - b.seat_number);
    const rightSeats = seatsData.filter(seat => seat.side === 'right')
        .sort((a, b) => a.row_number - b.row_number || a.seat_number - b.seat_number);
    
    // عرض المقاعد اليسرى
    renderSection(leftSection, leftSeats, 'يسار');
    
    // عرض المقاعد اليمنى
    renderSection(rightSection, rightSeats, 'يمين');
}

// عرض قسم من المقاعد
function renderSection(sectionElement, seats, sectionName) {
    sectionElement.innerHTML = '';
    
    const title = document.createElement('div');
    title.className = 'section-title';
    title.textContent = `الجانب ${sectionName}`;
    sectionElement.appendChild(title);
    
    // تجميع المقاعد حسب الصفوف
    const rows = {};
    seats.forEach(seat => {
        if (!rows[seat.row_number]) {
            rows[seat.row_number] = [];
        }
        rows[seat.row_number].push(seat);
    });
    
    // عرض كل صف
    Object.keys(rows).sort().forEach(rowNum => {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'row';
        
        const rowLabel = document.createElement('div');
        rowLabel.className = 'row-label';
        rowLabel.textContent = `صف ${rowNum}`;
        rowDiv.appendChild(rowLabel);
        
        rows[rowNum].forEach(seat => {
            const seatElement = createSeatElement(seat);
            rowDiv.appendChild(seatElement);
        });
        
        sectionElement.appendChild(rowDiv);
    });
}

// إنشاء عنصر مقعد
function createSeatElement(seat) {
    const seatDiv = document.createElement('div');
    seatDiv.className = `seat ${seat.status}`;
    if (seat.category === 'vip') {
        seatDiv.classList.add('vip');
    }
    
    seatDiv.textContent = seat.seat_number;
    seatDiv.dataset.seatId = seat.id;
    seatDiv.title = `مقعد ${seat.side === 'left' ? 'يسار' : 'يمين'} - صف ${seat.row_number} - مقعد ${seat.seat_number} (${seat.category === 'vip' ? 'VIP' : 'عادي'})`;
    
    // إضافة حدث النقر
    if (seat.status === 'available') {
        seatDiv.addEventListener('click', () => toggleSeatSelection(seat));
    }
    
    return seatDiv;
}

// تبديل اختيار المقعد
function toggleSeatSelection(seat) {
    const seatElement = document.querySelector(`[data-seat-id="${seat.id}"]`);
    
    if (selectedSeats.find(s => s.id === seat.id)) {
        // إلغاء الاختيار
        selectedSeats = selectedSeats.filter(s => s.id !== seat.id);
        seatElement.classList.remove('selected');
    } else {
        // اختيار المقعد - clear previous selection first (single seat booking)
        selectedSeats.forEach(selectedSeat => {
            const prevElement = document.querySelector(`[data-seat-id="${selectedSeat.id}"]`);
            if (prevElement) {
                prevElement.classList.remove('selected');
            }
        });
        selectedSeats = [seat]; // Replace with new selection
        seatElement.classList.add('selected');
    }
    
    updateBookingForm();
}

// تحديث نموذج الحجز
function updateBookingForm() {
    const bookingForm = document.getElementById('booking-form');
    const selectedSeatsDiv = document.getElementById('selected-seats');
    
    if (selectedSeats.length > 0) {
        bookingForm.style.display = 'block';
        
        const seatsText = selectedSeats.map(seat => 
            `${seat.side === 'left' ? 'يسار' : 'يمين'} - صف ${seat.row_number} - مقعد ${seat.seat_number}`
        ).join(', ');
        
        selectedSeatsDiv.innerHTML = `<strong>المقعد المختار:</strong> ${seatsText}`;
    } else {
        bookingForm.style.display = 'none';
    }
}

// إعداد مستمعي الأحداث
function setupEventListeners() {
    const bookingForm = document.getElementById('booking-form-element');
    bookingForm.addEventListener('submit', handleBooking);
}

// معالجة نموذج الحجز
async function handleBooking(event) {
    event.preventDefault();
    
    if (selectedSeats.length === 0) {
        showAlert('يرجى اختيار مقعد واحد على الأقل', 'error');
        return;
    }
    
    const customerName = document.getElementById('customer-name').value;
    const customerPhone = document.getElementById('customer-phone').value;
    
    if (!customerName || !customerPhone) {
        showAlert('يرجى ملء جميع الحقول', 'error');
        return;
    }
    
    // التحقق من صحة رقم الهاتف المصري
    const egyptianPhoneRegex = /^01[0125][0-9]{8}$/;
    if (!egyptianPhoneRegex.test(customerPhone)) {
        showAlert('يرجى إدخال رقم مصري صحيح (مثال: 01020158805)', 'error');
        return;
    }
    
    try {
        // API expects single seat_id, so we'll book the first selected seat
        // TODO: Modify API to support multiple seats booking
        const response = await fetch('/api/book-seat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                seat_id: selectedSeats[0].id,  // Send single seat_id instead of array
                customer_name: customerName,
                customer_phone: customerPhone
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('تم حجز المقعد بنجاح! سيتم مراجعة الحجز من قبل الإدارة.', 'success');
            
            // إعادة تعيين النموذج
            const bookingForm = document.getElementById('booking-form-element');
            bookingForm.reset();
            selectedSeats = [];
            
            // إعادة تحميل المقاعد
            setTimeout(() => {
                loadSeats();
                document.getElementById('booking-form').style.display = 'none';
            }, 2000);
        } else {
            showAlert(data.message || 'حدث خطأ في الحجز', 'error');
        }
    } catch (error) {
        console.error('خطأ في الحجز:', error);
        showAlert('حدث خطأ في إرسال الطلب', 'error');
    }
}

// عرض رسالة تنبيه
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // إزالة الرسالة بعد 5 ثواني
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// دالة لتحديث حالة المقعد (للاستخدام الإداري)
function updateSeatStatus(seatId, status) {
    const seatElement = document.querySelector(`[data-seat-id="${seatId}"]`);
    if (seatElement) {
        seatElement.className = `seat ${status}`;
        if (seatElement.classList.contains('vip')) {
            seatElement.classList.add('vip');
        }
    }
}