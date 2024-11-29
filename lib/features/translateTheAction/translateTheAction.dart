import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:http/http.dart' as http;
import 'dart:async';

Future<void> main1() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  final frontCamera = cameras.firstWhere(
    (camera) => camera.lensDirection == CameraLensDirection.front,
    orElse: () => cameras.first,
  );

  runApp(MyApp1(camera: frontCamera));
}

class MyApp1 extends StatelessWidget {
  final CameraDescription camera;

  MyApp1({required this.camera});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: CameraScreen(camera: camera),
    );
  }
}

class CameraScreen extends StatefulWidget {
  final CameraDescription camera;

  CameraScreen({required this.camera});

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  String _responseText = '';
  bool _isCapturing = false;
  Timer? _timer;
  final FlutterTts _flutterTts = FlutterTts();  // Initialized Text-to-Speech instance

  @override
  void initState() {
    super.initState();
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.high,
    );
    _initializeControllerFuture = _controller.initialize();
    _startFrameCapture();
  }

  @override
  void dispose() {
    _controller.dispose();
    _timer?.cancel();
    super.dispose();
  }

  void _startFrameCapture() {    
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      _captureAndSendImage();
    });
  }

  Future<void> _captureAndSendImage() async {
    if (_isCapturing) return;
    setState(() {
      _isCapturing = true;
    });

    try {
      await _initializeControllerFuture;
      final image = await _controller.takePicture();
      final bytes = await image.readAsBytes();
      final responseText = await sendImageToFlask(bytes);
      setState(() {
        _responseText = responseText;
      });
      _speakText(_responseText);  // Speak the response text
    } catch (e) {
      print(e);
    } finally {
      setState(() {
        _isCapturing = false;
      });
    }
  }

  Future<String> sendImageToFlask(Uint8List imageBytes) async {
    final String base64Image = base64Encode(imageBytes);
    final response = await http.post(
      Uri.parse('http://192.168.1.152:5001/process_frame'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'image': base64Image}),
    );

    if (response.statusCode == 200) {
      final responseData = jsonDecode(response.body);
      return responseData['text'];
    } else {
      return 'Failed to get text';
    }
  }

  // **Added method to speak the text aloud**
  void _speakText(String text) async {
    if (text.isNotEmpty) {
      await _flutterTts.setLanguage("en-US");  // Set language (optional)
      await _flutterTts.setPitch(1.0);  // Set pitch (optional)
      await _flutterTts.speak(text);  // Speak the text
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Camera')),
      body: Column(
        children: [
          Expanded(
            flex: 8, // Make the camera preview occupy most of the screen
            child: FutureBuilder<void>(
              future: _initializeControllerFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.done) {
                  return AspectRatio(
                    aspectRatio: _controller.value.aspectRatio,
                    child: CameraPreview(_controller),
                  );
                } else {
                  return Center(child: CircularProgressIndicator());
                }
              },
            ),
          ),
          Expanded(
            flex: 2, // Reserve a smaller section for the response text
            child: SingleChildScrollView(
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(
                  _responseText,
                  style: TextStyle(fontSize: 16),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}