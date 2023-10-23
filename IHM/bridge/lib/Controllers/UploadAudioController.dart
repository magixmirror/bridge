import 'package:bridge/Globals/Dialogs.dart';
import 'package:file_picker/file_picker.dart';
import 'package:get/get.dart' as GetX;
import 'package:web_socket_channel/web_socket_channel.dart';
import 'dart:io';
import 'dart:convert';

class UploadAudioController extends GetX.GetxController {
  PlatformFile? audio;
  WebSocketChannel? channel;
  GetX.RxString language = "en".obs;
  GetX.RxBool translating = false.obs;
  GetX.RxBool done_translating = false.obs;
  GetX.RxList<Map<String, dynamic>> result = <Map<String, dynamic>>[].obs;

  void reset() {
    channel = null;
    language.value = "en";
    translating.value = false;
    done_translating.value = false;
    result.value = [];
  }

  void translate() async {
    if (audio != null) {
      Dialogs.uploadingDialog();
      reset();
      channel = WebSocketChannel.connect(
        Uri.parse('ws://192.168.1.19:8764'),
      );
      File audioFile = File(audio!.path!);
      try {
        final fileStream = audioFile.openRead();
        await for (var chunk in fileStream) {
          channel?.sink.add(chunk);
        }
        channel?.sink.add("_DONE_");
        // Listen for result back
        channel?.stream.listen((message) {
          if (message is String) {
            if (message == "_UPLOAD_COMPLETE_") {
              GetX.Get.back();
              translating.value = true;
            } else if (message == "_DONE_") {
              channel?.sink.close();
            } else {
              result.value.add(jsonDecode(message) as Map<String, dynamic>);
            }
          }
        }, onDone: () {
          done_translating.value = true;
        });
      } catch (e) {
        print('Error sending video: $e');
        channel?.sink.close();
        GetX.Get.back();
        done_translating.value = true;
      }
    }
  }
}
