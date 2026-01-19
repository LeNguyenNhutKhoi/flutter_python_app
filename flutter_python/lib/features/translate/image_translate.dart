import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_python/appCore/page_option.dart';
import 'package:flutter_python/features/translate/translate_text_to_speech.dart';
import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';
import 'package:camera/camera.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:translator/translator.dart';

class CameraTextRecognitionPage extends StatefulWidget {
  const CameraTextRecognitionPage({super.key});

  @override
  _CameraTextRecognitionPageState createState() =>
      _CameraTextRecognitionPageState();
}

class _CameraTextRecognitionPageState
    extends State<CameraTextRecognitionPage> {
  late CameraController _cameraController;
  late List<CameraDescription> _cameras;
  bool _isCameraInitialized = false;
  bool _isProcessing = false;

  final FlutterTts _flutterTts = FlutterTts();
  String _recognizedText = "";
  String _translatedText = "";

  // Change to support multiple scripts
  TextRecognizer _textRecognizer =
      TextRecognizer(script: TextRecognitionScript.latin);

  final _translator = GoogleTranslator();
  int _selectedIndex = 0;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    _cameras = await availableCameras();
    _cameraController = CameraController(
      _cameras.first,
      ResolutionPreset.high,
      enableAudio: false,
    );
    await _cameraController.initialize();
    setState(() {
      _isCameraInitialized = true;
    });
  }

  Future<void> _captureAndRecognizeText() async {
    if (_isProcessing) return;

    setState(() {
      _isProcessing = true;
    });

    try {
      // Capture an image from the camera
      final imageFile = await _cameraController.takePicture();

      // Recognize text in the image
      final inputImage = InputImage.fromFilePath(imageFile.path);
      final RecognizedText recognizedText =
          await _textRecognizer.processImage(inputImage);

      setState(() {
        _recognizedText = recognizedText.text;
      });

      // Translate the recognized text to English
      await _translateText(_recognizedText);

      // Speak the translated text
      await _speak(_translatedText);
    } catch (e) {
      if (kDebugMode) {
        print("Error during text recognition: $e");
      }
    } finally {
      setState(() {
        _isProcessing = false;
      });
    }
  }

  Future<void> _translateText(String text) async {
    if (text.isEmpty) return;

    // Detect the Vietnamese language and translate to English
    final detectedLanguage = _detectLanguage(text);

    try {
      final translation = await _translator.translate(text, from: detectedLanguage, to: 'en');
      setState(() {
        _translatedText = translation.text;
      });
    } catch (e) {
      print("Error during translation: $e");
    }
  }

  String _detectLanguage(String text) {
    // Check for Vietnamese in the text
    if (RegExp(r'[\u00C0-\u1EF9]').hasMatch(text)) {
      // Vietnamese characters
      _textRecognizer = TextRecognizer(script: TextRecognitionScript.latin);
      return 'vi'; // Vietnamese
    }
    return 'en'; // Default to English if no match
  }

  // // Check for Vietnamese, Japanese, or Chinese in the text
  //   if (RegExp(r'[\u4E00-\u9FFF]').hasMatch(text)) {
  //     // Chinese characters
  //     _textRecognizer = TextRecognizer(script: TextRecognitionScript.chinese);
  //     return 'zh'; // Chinese
  //   } else if (RegExp(r'[\u3040-\u30FF\u31F0-\u31FF]').hasMatch(text)) {
  //     // Japanese characters
  //     _textRecognizer = TextRecognizer(script: TextRecognitionScript.japanese);
  //     return 'ja'; // Japanese
  //   } else if (RegExp(r'[\u00C0-\u1EF9]').hasMatch(text)) {
  //     // Vietnamese characters
  //     _textRecognizer = TextRecognizer(script: TextRecognitionScript.latin);
  //     return 'vi'; // Vietnamese
  //   }

  Future<void> _speak(String text) async {
    if (text.isEmpty) return;

    // Speak the translated text
    await _flutterTts.setLanguage("en-US");
    await _flutterTts.setPitch(1.0); // Adjust pitch as needed
    await _flutterTts.speak(text);
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });

    if (index == 0) {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => const SettingsPage()),
      );
    } else if (index == 1) {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => const TextToSpeechPage()),
      );
    }

    // // Navigate to another page
    // if (index == 1) {
    //   Navigator.push(
    //     context,
    //     MaterialPageRoute(builder: (context) => const SettingsPage()),
    //   );
    // }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Camera Text Recognition and Translation"),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // Camera preview or loading indicator
              if (_isCameraInitialized)
                SizedBox(
                  height: MediaQuery.of(context).size.height * 0.4,
                  child: ClipRect(
                    child: OverflowBox(
                      alignment: Alignment.center,
                      child: FittedBox(
                        fit: BoxFit.cover,
                        child: SizedBox(
                          width: _cameraController.value.previewSize!.height,
                          height: _cameraController.value.previewSize!.width,
                          child: CameraPreview(_cameraController),
                        ),
                      ),
                    ),
                  ),
                )
              else
                SizedBox(
                  height: MediaQuery.of(context).size.height * 0.4,
                  child: const Center(
                    child: CircularProgressIndicator(),
                  ),
                ),
              const SizedBox(height: 16),
              // Capture and Recognize button
              ElevatedButton(
                onPressed: _isProcessing ? null : _captureAndRecognizeText,
                child: Text(
                  _isProcessing ? "Processing..." : "Capture and Recognize Text",
                  style: const TextStyle(fontSize: 16),
                ),
              ),
              const SizedBox(height: 16),
              // Recognized Text display
              if (_recognizedText.isNotEmpty)
                const Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text(
                    "Recognized Text:",
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ),
              if (_recognizedText.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    _recognizedText,
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 16),
                  ),
                ),
              const SizedBox(height: 16),
              // Translated Text display
              if (_translatedText.isNotEmpty)
                const Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text(
                    "Translated Text:",
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ),
              if (_translatedText.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    _translatedText,
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 16, color: Colors.blue),
                  ),
                ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.arrow_back),
            label: 'Previous Page',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.arrow_forward),
            label: 'Text to Speech',
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _cameraController.dispose();
    _textRecognizer.close();
    _flutterTts.stop();
    super.dispose();
  }
}




