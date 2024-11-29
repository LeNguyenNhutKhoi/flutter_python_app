import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_python/appCore/constants/constants.dart';
import 'package:flutter_python/features/auth/controlller/auth_controller.dart';
import 'package:flutter_python/theme/pallete.dart';

class LogInButton extends ConsumerWidget {
  final bool isFromLogin;
  const LogInButton({Key? key, this.isFromLogin = true}) : super(key: key);

  void signInWithGoogle(BuildContext context, WidgetRef ref) {
    ref.read(authControllerProvider.notifier).signInWithGoogle(context, isFromLogin);
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Padding(
      padding: const EdgeInsets.all(18.0),
      child: ElevatedButton.icon(
        onPressed: () => signInWithGoogle(context, ref),
        icon: Image.asset(
          Constants.imageGooglePath,
          width: 35,
        ),
        label: const Text(
          'Press to log in by Google',
          style: TextStyle(fontSize: 18),
        ),
        style: ElevatedButton.styleFrom(
          backgroundColor: Pallete.greyColor,
          minimumSize: const Size(double.infinity, 50),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
        ),
      ),
    );
  }
}
