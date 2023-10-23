import 'package:get/get.dart' as GetX;
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';




class HomeController extends GetX.GetxController{



  Future<PlatformFile?> pickAudio() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.audio,
      allowMultiple: false,
    );
    if (result != null) {
      return result.files.first;
    }
    return null;
  }

  Future<PlatformFile?> pickVideo() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.video,
      allowMultiple: false,
    );
    if (result != null) {
      return result.files.first;
    }
    return null;
  }
}

