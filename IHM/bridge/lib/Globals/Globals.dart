import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:get/get.dart' as GetX;

class Globals{
  static const Color color1 = Color(0xFF231D3C);
  static const Color color2 = Color(0xFF918BB5);
  static const Color colorBlack = Color(0xFF3B3B3B);
  static const Color color_live_audio = Color(0xFF84a59d);
  static const Color color_upload_audio = Color(0xFFf28482);
  static const Color color_live_video = Color(0xFFf6bd60);
  static const Color color_upload_video = Color(0xFF0096c7);
  static final double dimension = sqrt(pow(GetX.Get.width, 2) + pow(GetX.Get.height, 2));
}