import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';

class TextToSpeechPage extends StatefulWidget {
  const TextToSpeechPage({super.key});

  @override
  _TextToSpeechPageState createState() => _TextToSpeechPageState();
}

class _TextToSpeechPageState extends State<TextToSpeechPage> {
  final FlutterTts _flutterTts = FlutterTts();
  final TextEditingController _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  // Function to start speaking the text
  void _speak() async {
    String text = _controller.text;
    if (text.isNotEmpty) {
      await _flutterTts.setLanguage("en-US");
      await _flutterTts.setSpeechRate(0.5); // Optional, adjust speech rate
      await _flutterTts.speak(text);
    } else {
      // Optionally, show a message if the text is empty
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please enter some text to speak")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Text to Speech"),
        backgroundColor: Colors.blueAccent,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              "Enter text and press the button to hear it:",
              style: TextStyle(fontSize: 18),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 20),
            // Text Input for user input
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Enter English Text',
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 20),
            // Button to trigger text-to-speech
            ElevatedButton(
              onPressed: _speak,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green[50],
                padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 24),
                textStyle: const TextStyle(fontSize: 16),
              ),
              child: const Text("Convert to Speech"),
            ),
          ],
        ),
      ),
    );
  }
}

