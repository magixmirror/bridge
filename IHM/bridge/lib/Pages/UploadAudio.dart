import 'package:bridge/Globals/Globals.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' as GetX;
import 'package:bridge/Controllers/UploadAudioController.dart';
import 'package:chat_bubbles/chat_bubbles.dart';
import 'package:flutter_speed_dial/flutter_speed_dial.dart';
import 'package:lottie/lottie.dart';
import 'package:bridge/Globals/Dialogs.dart';

class UploadAudio extends StatelessWidget {
  UploadAudio({Key? key, required this.audio}) : super(key: key);
  final PlatformFile audio;
  @override
  Widget build(BuildContext context) {
    final UploadAudioController controller =
    GetX.Get.put(UploadAudioController());
    controller.audio = audio;
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(Globals.dimension * 0.01),
          child: Center(
            child: Column(
              children: <Widget>[
                Align(
                  alignment: Alignment.centerLeft,
                  child: IconButton(
                      onPressed: () {
                        controller.reset();
                        GetX.Get.back();
                      },
                      icon: const Icon(Icons.arrow_back_ios_new_rounded)),
                ),
                CircleAvatar(
                  radius: Globals.dimension * 0.06,
                  backgroundColor: Globals.color_upload_audio,
                  child: Padding(
                    padding: EdgeInsets.all(Globals.dimension * 0.02),
                    child: const Image(
                      image: AssetImage("assets/upload_video.png"),
                    ),
                  ),
                ),
                SizedBox(height: Globals.dimension * 0.02),
                Text(audio.name,
                    textAlign: TextAlign.center,
                    overflow: TextOverflow.ellipsis,
                    maxLines: 2,
                    style: TextStyle(
                        fontWeight: FontWeight.w500,
                        fontSize: Globals.dimension * 0.018)),
                SizedBox(height: Globals.dimension * 0.02),
                const Divider(),
                GetX.Obx(() {
                  if (controller.result.isEmpty && controller.translating.isFalse) {
                    return const Expanded(
                      child: Center(
                          child: Text(
                            "Translation will appear here",
                            textAlign: TextAlign.center,
                            style: TextStyle(color: Colors.grey),
                          )),
                    );
                  } else {
                    return Expanded(
                      child: SingleChildScrollView(
                        padding: EdgeInsets.symmetric(
                            vertical: Globals.dimension * 0.02),
                        scrollDirection: Axis.vertical,
                        child: Column(
                            children: <Widget>[] +
                                controller.result.value
                                    .map((r) => Column(
                                  children: [
                                    BubbleSpecialThree(
                                      sent: true,
                                      text: r.containsKey("audio")
                                          ? r["audio"][
                                      controller.language.value]
                                          : r["sign language"][
                                      controller
                                          .language.value],
                                      color: r.containsKey("audio")
                                          ? const Color(0xFF212529)
                                          : const Color(0xFFE8E8EE),
                                      tail: false,
                                      isSender: r.containsKey("audio")
                                          ? true
                                          : false,
                                      textStyle: TextStyle(
                                          height: 1.25,
                                          color: r.containsKey("audio")
                                              ? Colors.grey[300]
                                              : Colors.black),
                                    ),
                                    SizedBox(
                                        height:
                                        Globals.dimension * 0.02)
                                  ],
                                ))
                                    .toList() +
                                [
                                  controller.translating.isTrue
                                      ? Lottie.network(
                                      "https://lottie.host/250aecd3-affd-4170-b90d-2abd664c8aff/Y6iLsMoEUA.json",
                                      width: Globals.dimension * 0.05)
                                      : const SizedBox.shrink()
                                ]),
                      ),
                    );
                  }
                }),
                const Divider(),
                SizedBox(height: Globals.dimension * 0.02),
                Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      /*ElevatedButton(
                          onPressed: () {},
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Globals.color_upload_video,
                            padding: EdgeInsets.all(Globals.dimension * 0.015),
                            shape: const CircleBorder(),
                            elevation: 1,
                          ),
                          child: Center(
                              child: Icon(Icons.multitrack_audio_rounded,
                                  color: Colors.white,
                                  size: Globals.dimension * 0.03))),
                      SizedBox(width: Globals.dimension * 0.02),*/
                      ElevatedButton(
                          onPressed: () {
                            controller.translate();
                          },
                          style: OutlinedButton.styleFrom(
                            backgroundColor: Globals.color_upload_audio,
                            padding: EdgeInsets.symmetric(
                                vertical: Globals.dimension * 0.02,
                                horizontal: Globals.dimension * 0.04),
                          ),
                          child: const Text(
                            'Translate video',
                            style: TextStyle(color: Colors.white),
                          )),
                      SizedBox(width: Globals.dimension * 0.02),
                      SpeedDial(
                        backgroundColor: Globals.color_upload_audio,
                        foregroundColor: Colors.white,
                        curve: Curves.bounceIn,
                        animatedIcon: AnimatedIcons.menu_close,
                        children: [
                          SpeedDialChild(
                              child: CircleAvatar(
                                  child: ClipOval(
                                    child: Image.asset(
                                      'assets/en.png',
                                      width: 100,
                                      // Set the desired width (must be the same as the height)
                                      height: 100,
                                      // Set the desired height (must be the same as the width)
                                      fit: BoxFit
                                          .cover, // Set the fit property to BoxFit.cover or another value
                                    ),
                                  ) // Set the fit property to BoxFit.cover or another value
                              ),
                              label: "English",
                              onTap: () => controller.language.value = "en"),
                          SpeedDialChild(
                              child: CircleAvatar(
                                  child: ClipOval(
                                    child: Image.asset(
                                      'assets/fr.png',
                                      width: 100,
                                      // Set the desired width (must be the same as the height)
                                      height: 100,
                                      // Set the desired height (must be the same as the width)
                                      fit: BoxFit
                                          .cover, // Set the fit property to BoxFit.cover or another value
                                    ),
                                  ) // Set the fit property to BoxFit.cover or another value
                              ),
                              label: "French",
                              onTap: () => controller.language.value = "fr"),
                          SpeedDialChild(
                              child: CircleAvatar(
                                  child: ClipOval(
                                    child: Image.asset(
                                      'assets/de.png',
                                      width: 100,
                                      // Set the desired width (must be the same as the height)
                                      height: 100,
                                      // Set the desired height (must be the same as the width)
                                      fit: BoxFit
                                          .cover, // Set the fit property to BoxFit.cover or another value
                                    ),
                                  ) // Set the fit property to BoxFit.cover or another value
                              ),
                              label: "German",
                              onTap: () => controller.language.value = "de"),
                          SpeedDialChild(
                              child: CircleAvatar(
                                  child: ClipOval(
                                    child: Image.asset(
                                      'assets/it.png',
                                      width: 100,
                                      // Set the desired width (must be the same as the height)
                                      height: 100,
                                      // Set the desired height (must be the same as the width)
                                      fit: BoxFit
                                          .cover, // Set the fit property to BoxFit.cover or another value
                                    ),
                                  ) // Set the fit property to BoxFit.cover or another value
                              ),
                              label: "Italian",
                              onTap: () => controller.language.value = "it"),
                          SpeedDialChild(
                              child: CircleAvatar(
                                  child: ClipOval(
                                    child: Image.asset(
                                      'assets/es.png',
                                      width: 100,
                                      // Set the desired width (must be the same as the height)
                                      height: 100,
                                      // Set the desired height (must be the same as the width)
                                      fit: BoxFit
                                          .cover, // Set the fit property to BoxFit.cover or another value
                                    ),
                                  ) // Set the fit property to BoxFit.cover or another value
                              ),
                              label: "Spanish",
                              onTap: () => controller.language.value = "es")
                        ],
                      ),
                    ]),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
