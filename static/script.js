const slider = document.getElementById('slider');
noUiSlider.create(slider, { start: [1,5], connect: true, range: { 'min': 0, 'max': 10 } });

const video = document.getElementById('video');
const canvas = document.getElementById('overlay');
const ctx = canvas.getContext('2d');
const badge = document.getElementById('countBadge');
const items = Array.from(document.querySelectorAll('.menu-item'));
const progress = {};
items.forEach(item => progress[item.dataset.index] = 0);

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => { video.srcObject = stream; })
  .catch(err => console.error(err));
video.addEventListener('loadeddata', () => { canvas.width = video.videoWidth; canvas.height = video.videoHeight; });

const hands = new Hands({ locateFile: f => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${f}` });
hands.setOptions({ maxNumHands: 2, modelComplexity: 1, minDetectionConfidence: 0.7, minTrackingConfidence: 0.5 });
hands.onResults(onResults);
new Camera(video, { onFrame: async () => await hands.send({ image: video }), width: 640, height: 480 }).start();

function onResults(results) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  let totalFingers = 0;
  if (results.multiHandLandmarks) {
    results.multiHandLandmarks.forEach((lm, idx) => {
      let handedness = results.multiHandedness?.[idx]?.label || 'Right';
      let count = 0;
      [8,12,16,20].forEach(i => { if (lm[i].y < lm[i-2].y) count++; });
      if ((handedness === 'Right' && lm[4].x < lm[3].x) || (handedness === 'Left' && lm[4].x > lm[3].x)) count++;
      totalFingers += count;
      drawConnectors(ctx, lm, HAND_CONNECTIONS, { color: '#00FF00', lineWidth: 2 });
      drawLandmarks(ctx, lm, { color: '#FF0000', lineWidth: 1, radius: 4 });
    });
  }
  badge.textContent = `Fingers: ${totalFingers}`;

  items.forEach(item => {
    const idx = parseInt(item.dataset.index, 10);
    const progEl = item.querySelector('.select-progress');
    if (totalFingers === idx) {
      progress[idx] = Math.min(progress[idx] + 0.02, 1);
    } else {
      progress[idx] = 0;
      item.classList.remove('selected');
    }
    progEl.style.width = `${progress[idx]*100}%`;
    if (progress[idx] >= 1 && !item.classList.contains('selected')) {
      item.classList.add('selected');
      pickItem(idx);
    }
  });
}
const urlMap = {
  1: '/order/phobo',
  2: '/order/buncha',
  3: '/order/bunbo',
  4: '/order/comtam',
  5: '/order/bundau',
  6: '/order/burger',
  7: '/order/garan',
  8: '/order/suonnuong',
  9: '/order/canhkimchi',
  10: '/order/hutieu',
}
// Hàm xử lý khi món được chọn
function pickItem(idx) {
  console.log(`Món ${idx} đã được chọn`);
  // Lưu lựa chọn (ví dụ push vào mảng)
  //selections.push(idx);
  // Chuyển UI sang trạng thái order tiếp theo
  // Ví dụ: window.location.href = `/order/${idx}`;
  // Hoặc hiển thị form order
  const nextUrl = urlMap[idx] || '/';
  window.location.href = nextUrl;
}

      if ((handedness === 'Right' && lm[4].x < lm[3].x) || (handedness === 'Left' && lm[4].x > lm[3].x)) count++;
      totalFingers += count;
      drawConnectors(ctx, lm, HAND_CONNECTIONS, { color: '#00FF00', lineWidth: 2 });
      drawLandmarks(ctx, lm, { color: '#FF0000', lineWidth: 1, radius: 4 });
 
  badge.textContent = `Fingers: ${totalFingers}`;

  items.forEach(item => {
    const idx = parseInt(item.dataset.index, 10);
    const progEl = item.querySelector('.select-progress');
    if (totalFingers === idx) {
      progress[idx] = Math.min(progress[idx] + 0.02, 1);
    } else {
      progress[idx] = 0;
      item.classList.remove('selected');
    }
    progEl.style.width = `${progress[idx]*100}%`;
    if (progress[idx] >= 1) item.classList.add('selected');
  });

