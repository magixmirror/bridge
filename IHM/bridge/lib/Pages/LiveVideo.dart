import 'package:flutter/material.dart';
import 'package:get/get.dart' as GetX;
import 'package:bridge/Controllers/LiveVideoController.dart';
import 'package:camera/camera.dart';
import 'package:bridge/Globals/Globals.dart';
import 'package:flutter_speed_dial/flutter_speed_dial.dart';

class LiveVideo extends StatelessWidget {
  LiveVideo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final LiveVideoController controller = GetX.Get.put(LiveVideoController());
    return Scaffold(
      body: GetX.Obx(() {
        if(controller.cameraStarted.isTrue){
          return Stack(
            children: [
              ClipRect(
                clipper: _MediaSizeClipper(controller.mediaSize),
                child: Transform.scale(
                  scale: controller.cameraScale.value,
                  alignment: Alignment.topCenter,
                  child: CameraPreview(controller.cameraController!),
                ),
              ),
              Column(children: [
                const Expanded(child: SizedBox.shrink()),
                Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      ElevatedButton(
                          onPressed: () {},
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Globals.color_live_video,
                            padding: EdgeInsets.all(Globals.dimension * 0.015),
                            shape: const CircleBorder(),
                            elevation: 1,
                          ),
                          child: Center(
                              child: Icon(Icons.multitrack_audio_rounded,
                                  color: Colors.white,
                                  size: Globals.dimension * 0.03))),
                      SizedBox(width: Globals.dimension * 0.02),
                      ElevatedButton(
                          onPressed: () {
                            controller.toggleRecording();
                          },
                          style: OutlinedButton.styleFrom(
                            backgroundColor: Globals.color_live_video,
                            padding: EdgeInsets.symmetric(
                                vertical: Globals.dimension * 0.02,
                                horizontal: Globals.dimension * 0.04),
                          ),
                          child: Text(
                            controller.recording.isFalse ?
                            'Start recording' : 'Stop recording',
                            style: const TextStyle(color: Colors.white),
                          )),
                      SizedBox(width: Globals.dimension * 0.02),
                      SpeedDial(
                        backgroundColor: Globals.color_live_video,
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
                SizedBox(height: Globals.dimension * 0.02)
              ],)
            ],
          );
        }else{
          return const Center(child: CircularProgressIndicator());
        }
      }),);
  }
}

class _MediaSizeClipper extends CustomClipper<Rect> {
  final Size mediaSize;
  const _MediaSizeClipper(this.mediaSize);
  @override
  Rect getClip(Size size) {
    return Rect.fromLTWH(0, 0, mediaSize.width, mediaSize.height);
  }
  @override
  bool shouldReclip(CustomClipper<Rect> oldClipper) {
    return true;
  }
}
