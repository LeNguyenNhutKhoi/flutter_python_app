import 'package:flutter/material.dart';

class InfoPage extends StatefulWidget {
  const InfoPage({super.key});

  @override
  _InfoPageState createState() => _InfoPageState();
}

class _InfoPageState extends State<InfoPage> {
  String displayedContent = ""; // Variable to hold the text content

  // Example content for the buttons
  final Map<String, String> contentMap = {
    "Terms of Service":
        "Terms of Service: \n"
        "1. By using our social media app, you agree to take responsibility for your account's security and actions.\n"
        "2. Content you share remains your property, but you grant us permission to use it to deliver app features and services.\n"
        "3. You must not post harmful, offensive, or illegal content, as doing so may result in suspension or termination of your account.\n"
        "4. While our sign language translation aims for accuracy, occasional errors may occur.\n"
        "5. Continued use of the app indicates acceptance of these terms, including any future updates.",
    "Privacy Policy":
        "Privacy Policy: \n"
        "1. The app value your privacy and collect only necessary information, such as your name, email, and usage data, to enhance your experience.\n"
        "2. Your data is securely stored and never sold to third parties.\n"
        "3. Camera access is used strictly for sign language recognition.\n"
        "4. By using the app, you agree to this privacy policy and any future amendments.",
    "Community Standards":
        "Community Standards: \n"
        "1. The app fosters a respectful and inclusive community where all users are treated with dignity.\n"
        "2. We encourage the sharing of appropriate content while strictly prohibiting harmful, offensive, or illegal material.\n"
        "3. Users are expected to act responsibly, avoid spreading misinformation, and refrain from abusive behavior.\n"
        "4. By supporting sign language communication, you contribute to a welcoming and accessible environment.\n"
        "5. Report violations to help maintain a safe and positive space for everyone.",
    };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Policies and Standards", style: Theme.of(context).textTheme.bodyLarge ,),
        backgroundColor: Colors.blueAccent,
      ),
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Text(
                displayedContent,
                style: const TextStyle(fontSize: 16.0),
              ),
            ),
          ),
        ],
      ),
      floatingActionButton: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          FloatingActionButton(
            onPressed: () {
              setState(() {
                displayedContent = contentMap["Terms of Service"]!;
              });
            },
            tooltip: "Terms of Service",
            backgroundColor: Colors.blue,
            child: Center(
              child: Text(
                "Terms of Service",
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(fontSize: 10), 
              ),
            ),
          ),
          const SizedBox(height: 16),
          FloatingActionButton(
            onPressed: () {
              setState(() {
                displayedContent = contentMap["Privacy Policy"]!;
              });
            },
            tooltip: "Privacy Policy",
            backgroundColor: Colors.blue,
            child: Container(
              alignment: Alignment.center,
              child: Text(
                "Privacy Policy",
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(fontSize: 10),
              ),
            ),
          ),
          const SizedBox(height: 16),
          FloatingActionButton(
            onPressed: () {
              setState(() {
                displayedContent = contentMap["Community Standards"]!;
              });
            },
            tooltip: "Community Standards",
            backgroundColor: Colors.blue,
            child: Center(
              child: Text(
                "Community Standards",
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(fontSize: 9),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
