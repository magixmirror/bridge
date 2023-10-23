import 'dart:async';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:flutter/material.dart' as material;
import 'package:get/get.dart' as GetX;
import 'package:camera/camera.dart';
import 'package:record/record.dart';

class LiveVideoController extends GetX.GetxController {
  CameraController? cameraController;
  GetX.RxString language = "en".obs;
  GetX.RxBool cameraStarted = false.obs;
  GetX.RxBool recording = false.obs;
  late XFile video;
  final audioRecorder = AudioRecorder();
  GetX.RxDouble cameraScale = (0.0).obs;
  material.Size mediaSize = material.Size(GetX.Get.width, GetX.Get.height);
  WebSocketChannel? videoChannel;
  WebSocketChannel? audioChannel;
  GetX.RxList<Map<String, dynamic>> result = <Map<String, dynamic>>[].obs;

  @override
  void onReady() {
    super.onReady();
    // Get the list of available cameras
    availableCameras().then((cameras) {
      if (cameras.isEmpty) {
        print('No cameras available');
      } else {
        // Initialize the first camera from the list
        cameraController =
            CameraController(cameras[0], ResolutionPreset.low);
        cameraController!.initialize().whenComplete(() => {
              cameraScale.value = 1 /
                  (cameraController!.value.aspectRatio * mediaSize.aspectRatio),
              cameraStarted.value = true
            });
      }
    });
  }


  @override
  void onClose() {
    if (recording.isTrue) {
      stopRecording();
    }
    cameraController!.dispose();
    GetX.Get.delete<LiveVideoController>;
    super.onClose();
  }

  void toggleRecording() {
    if (recording.isTrue) {
      stopRecording();
    } else {
      startRecording();
    }
  }

  void startRecording() {
    startVideoRecording();
    startAudioRecording();
    recording.value = true;
  }

  void stopRecording() {
    stopVideoRecording();
    stopAudioRecording();
    recording.value = false;
  }

  Future<void> startVideoRecording() async {
    try {
      await cameraController!.startVideoRecording();
    } catch (e) {
      print('Error starting video recording: $e');
    }
  }

  Future<void> stopVideoRecording() async {
    try {
      // Stop recording and retrieve the video file
      XFile video = await cameraController!.stopVideoRecording();
      //print('Video saved to ${videoFile.path}');
    } catch (e) {
      print('Error stopping video recording: $e');
    }
  }

  Future<void> startAudioRecording() async {
    if (await audioRecorder.hasPermission()) {
      final audioStream = await audioRecorder.startStream(const RecordConfig(encoder: AudioEncoder.aacLc));
    }
  }

  Future<void> stopAudioRecording() async {
    try {
      await audioRecorder.stop();
    } catch (e) {
      print('Error stopping audio recording: $e');
    }
  }
}
