import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_python/features/translate/image_translate.dart';
import 'package:flutter_python/features/translate/translate_text_to_speech.dart';
import 'package:flutter_python/features/translateTheAction/translateTheAction.dart';

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Translate option"),
        backgroundColor: Colors.blueAccent,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start, // Align content at the top
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const SizedBox(height: 30),
            // Page Title
            Text(
              "Choose type to translate",
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Colors.blueAccent,
                  ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 40),
            
            // First Button
            _buildCustomButton(
              context,
              label: "Translate text from image",
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const CameraTextRecognitionPage()),
                );
              },
            ),

            const SizedBox(height: 20),

            // Second Button
            _buildCustomButton(
              context,
              label: "Convert text to speech",
              onPressed: () {
                // Navigate to Page 2 when clicked
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const TextToSpeechPage()),
                );
              },
            ),

            const SizedBox(height: 20),

            // Third Button
            _buildCustomButton(
              context,
              label: "Translate Sign Language",
              onPressed: () async {
                // Fetch available cameras
                final cameras = await availableCameras();

                // Find the front camera or use the first available one
                final frontCamera = cameras.firstWhere(
                  (camera) => camera.lensDirection == CameraLensDirection.front,
                  orElse: () => cameras.first,
                );

                // Navigate to MyApp1 with the selected camera
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => MyApp1(camera: frontCamera),
                  ),
                );
              },
            ),
            const SizedBox(height: 20),

          ],
        ),
      ),
    );
  }

  // Custom Button Style
  Widget _buildCustomButton(
      BuildContext context, {
        required String label,
        required VoidCallback onPressed,
      }) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.blueAccent, // Button color
        minimumSize: const Size(double.infinity, 50), // Full width button
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(15), // Rounded corners
        ),
        padding: const EdgeInsets.symmetric(vertical: 15),
      ),
      child: Text(
        label,
        style: const TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.w600,
          color: Colors.black, // Set text color to black
        ),
      ),
    );
  }
}

// Page 1
class Page1 extends StatelessWidget {
  const Page1({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Page 1"),
        backgroundColor: Colors.blueAccent,
      ),
      body: const Center(
        child: Text("This is Page 1", style: TextStyle(fontSize: 18)),
      ),
    );
  }
}

// Page 2
class Page2 extends StatelessWidget {
  const Page2({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Page 2"),
        backgroundColor: Colors.blueAccent,
      ),
      body: const Center(
        child: Text("This is Page 2", style: TextStyle(fontSize: 18)),
      ),
    );
  }
}

// Page 3
class Page3 extends StatelessWidget {
  const Page3({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Page 3"),
        backgroundColor: Colors.blueAccent,
      ),
      body: const Center(
        child: Text("This is Page 3", style: TextStyle(fontSize: 18)),
      ),
    );
  }
}

