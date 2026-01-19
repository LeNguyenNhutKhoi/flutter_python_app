import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_python/appCore/common/loader.dart';
import 'package:flutter_python/appCore/common/sign_in_button.dart';
import 'package:flutter_python/appCore/constants/constants.dart';
import 'package:flutter_python/features/auth/controlller/auth_controller.dart';
import 'package:flutter_python/responsive/responsive.dart';

class LoginScreen extends ConsumerWidget {
  const LoginScreen({super.key});

  void signInAsGuest(WidgetRef ref, BuildContext context) {
    ref.read(authControllerProvider.notifier).signInAsGuest(context);
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isLoading = ref.watch(authControllerProvider);

    return Scaffold(
      appBar: AppBar(
        title: Image.asset(
          Constants.appLogoPath,
          height: 40,
        ),
      ),
      body: isLoading
          ? const Loader()
          : Column(
              children: [
                const SizedBox(height: 30),
                const Text(
                  'Welcome, please login',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 0.5,
                  ),
                ),
                const SizedBox(height: 30),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Image.asset(
                    Constants.imageLoginPath,
                    height: 400,
                  ),
                ),
                const SizedBox(height: 20),
                const Responsive(child: LogInButton()),
              ],
            ),
    );
  }
}
