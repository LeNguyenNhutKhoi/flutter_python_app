import 'package:dcdg/dcdg.dart';
import 'package:flutter/material.dart';
import 'package:flutter_python/features/translate/image_translate.dart';
import 'package:flutter_python/theme/pallete.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter_python/features/translate/translate_text_to_speech.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_python/appCore/common/error_text.dart';
import 'package:flutter_python/appCore/common/loader.dart';
import 'package:flutter_python/features/auth/controlller/auth_controller.dart';
import 'package:flutter_python/firebase_options.dart';
import 'package:flutter_python/models/user_model.dart';
import 'package:flutter_python/router.dart';
import 'package:routemaster/routemaster.dart';

import 'package:flutter/material.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}

class MyApp extends ConsumerStatefulWidget {
  const MyApp({super.key});

  @override
  ConsumerState<ConsumerStatefulWidget> createState() => _MyAppState();
}

class _MyAppState extends ConsumerState<MyApp> {
  UserModel? userModel;

  void getData(WidgetRef ref, User data) async {
    userModel = await ref
        .watch(authControllerProvider.notifier)
        .getUserData(data.uid)
        .first;
    ref.read(userProvider.notifier).update((state) => userModel);
  }

  @override
  Widget build(BuildContext context) {
    return ref.watch(authStateChangeProvider).when(
          data: (data) => MaterialApp.router(
            debugShowCheckedModeBanner: false,
            title: 'Social media app',
            theme: ref.watch(themeNotifierProvider),
            routerDelegate: RoutemasterDelegate(
              routesBuilder: (context) {
                if (data != null) {
                  getData(ref, data);
                  if (userModel != null) {
                    return loggedInRoute;
                  }
                }
                return loggedOutRoute;
              },
            ),
            routeInformationParser: const RoutemasterParser(),
          ),
          error: (error, stackTrace) => ErrorText(error: error.toString()),
          loading: () => const Loader(),
        );
  }
}



// class HomePage extends StatelessWidget {
//   const HomePage({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         title: const Text('Home Page'),
//       ),
//       body: Center(
//         child: ElevatedButton(
//           onPressed: () {
//             // Navigate to SecondPage when the button is pressed
//             Navigator.push(
//               context,
//               MaterialPageRoute(builder: (context) => const SecondPage()),
//             );
//           },
//           child: const Text('Go to Second Page'),
//         ),
//       ),
//     );
//   }
// }

// class SecondPage extends StatelessWidget {
  
// class MyApp extends ConsumerStatefulWidget {
//   const MyApp({super.key});

//   @override
//   ConsumerState<ConsumerStatefulWidget> createState() => _MyAppState();
// }

// class _MyAppState extends ConsumerState<MyApp> {
//   UserModel? userModel;

//   void getData(WidgetRef ref, User data) async {
//     userModel = await ref
//         .watch(authControllerProvider.notifier)
//         .getUserData(data.uid)
//         .first;
//     ref.read(userProvider.notifier).update((state) => userModel);
//   }

//   @override
//   Widget build(BuildContext context) {
//     return ref.watch(authStateChangeProvider).when(
//           data: (data) => MaterialApp.router(
//             debugShowCheckedModeBanner: false,
//             title: 'Social media',
//             theme: ref.watch(themeNotifierProvider),
//             routerDelegate: RoutemasterDelegate(
//               routesBuilder: (context) {
//                 if (data != null) {
//                   getData(ref, data);
//                   if (userModel != null) {
//                     return loggedInRoute;
//                   }
//                 }
//                 return loggedOutRoute;
//               },
//             ),
//             routeInformationParser: const RoutemasterParser(),
//           ),
//           error: (error, stackTrace) => ErrorText(error: error.toString()),
//           loading: () => const Loader(),
//         );
//   }
// }


