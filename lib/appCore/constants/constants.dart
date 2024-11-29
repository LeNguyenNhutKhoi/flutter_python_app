import 'package:flutter/material.dart';
import 'package:flutter_python/features/feed/feed_screen.dart';
import 'package:flutter_python/features/home/screens/home_screen.dart';
import 'package:flutter_python/features/post/screens/add_post_screen.dart';
import 'package:flutter_python/features/translate/translate_text_to_speech.dart';
import 'package:flutter_python/features/translate/translate_text_to_speech.dart';

class Constants {
  static const appLogoPath = 'asset/image/schaleLogo.png'; // const cause this is contants
  static const imageLoginPath = 'asset/image/millenniumLogo.png';
  static const imageGooglePath = 'asset/image/google.png';

  static const bannerDefault = 'https://www.shutterstock.com/image-vector/default-ui-image-placeholder-wireframes-600nw-1037719192.jpg';
  static const avatarDefault = 'https://www.doccen.vn/icons/default-group-avatar.svg';

  static var tabWidgets = [
    const FeedScreen(),
    const AddPostScreen(),
  ];

  static const IconData   up = IconData(0xe800, fontFamily: 'MyFlutterApp', fontPackage: null);
  static const IconData down = IconData(0xe801, fontFamily: 'MyFlutterApp', fontPackage: null);

  static const awardsPath = 'asset/image/awards';

  static const awards = {
    'awesomeAns': '${Constants.awardsPath}/awesomeanswer.png',
    'gold': '${Constants.awardsPath}/gold.png',
    'platinum': '${Constants.awardsPath}/platinum.png',
    'helpful': '${Constants.awardsPath}/helpful.png',
    'plusone': '${Constants.awardsPath}/plusone.png',
    'rocket': '${Constants.awardsPath}/rocket.png',
    'thankyou': '${Constants.awardsPath}/thankyou.png',
    'til': '${Constants.awardsPath}/til.png',
  };
}