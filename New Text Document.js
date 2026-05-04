window.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    body.style.margin = '0';
    body.style.display = 'flex';
    body.style.justifyContent = 'center';
    body.style.alignItems = 'center';
    body.style.height = '100vh';
    body.style.background = '#111';

    const canvas = document.createElement('canvas');
    canvas.width = 320;
    canvas.height = 320;
    body.appendChild(canvas);

    const ctx = canvas.getContext('2d');

    function drawAnalogDate() {
        const now = new Date();
        const radius = canvas.width / 2;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.save();
        ctx.translate(radius, radius);

        // Outer circle
        ctx.beginPath();
        ctx.arc(0, 0, radius - 10, 0, 2 * Math.PI);
        ctx.fillStyle = '#0d0d0d';
        ctx.fill();
        ctx.lineWidth = 8;
        ctx.strokeStyle = '#444';
        ctx.stroke();

        // Draw tick marks for date positions
        const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
        for (let day = 1; day <= daysInMonth; day++) {
            const angle = (day / daysInMonth) * 2 * Math.PI - Math.PI / 2;
            const inner = radius - 30;
            const outer = radius - 18;
            ctx.beginPath();
            ctx.moveTo(Math.cos(angle) * inner, Math.sin(angle) * inner);
            ctx.lineTo(Math.cos(angle) * outer, Math.sin(angle) * outer);
            ctx.strokeStyle = day === now.getDate() ? '#ffcc00' : '#666';
            ctx.lineWidth = day === now.getDate() ? 4 : 2;
            ctx.stroke();
        }

        // Draw date hand
        const dateAngle = (now.getDate() / daysInMonth) * 2 * Math.PI - Math.PI / 2;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(Math.cos(dateAngle) * (radius - 70), Math.sin(dateAngle) * (radius - 70));
        ctx.strokeStyle = '#ffcc00';
        ctx.lineWidth = 6;
        ctx.stroke();

        // Center dot
        ctx.beginPath();
        ctx.arc(0, 0, 7, 0, 2 * Math.PI);
        ctx.fillStyle = '#ffcc00';
        ctx.fill();

        // Date label in center
        const monthNames = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        const dateText = `${monthNames[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()}`;
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 16px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(dateText, 0, 0);

        ctx.restore();
    }

    drawAnalogDate();
    setInterval(drawAnalogDate, 1000);
});