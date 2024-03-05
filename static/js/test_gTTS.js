const gtts = require('gtts');

const text = 'Xin chào, bạn khỏe không?'; // Vietnamese text

const tts = new gtts(text, 'vi'); // Pass the language code as the second argument

tts.save('output.mp3', function (err, result) {
  if (err) {
    throw new Error(err);
  }
  console.log('Speech saved!');
});