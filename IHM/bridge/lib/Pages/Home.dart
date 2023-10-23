import 'package:bridge/Pages/UploadVideo.dart';
import 'package:bridge/Pages/UploadAudio.dart';
import 'package:bridge/Pages/LiveVideo.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' as GetX;
import 'package:bridge/Controllers/HomeController.dart';
import 'package:bridge/Globals/Globals.dart';
import 'package:bridge/Globals/MyTabBar.dart';

class Home extends StatelessWidget {
  Home({Key? key}) : super(key: key);
  final HomeController controller = GetX.Get.put(HomeController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(Globals.dimension * 0.01),
          child: Center(
            child: Column(
              children: [
                Expanded(
                    flex: 1,
                    child: Center(
                      child: Image(
                        image: const AssetImage("assets/Logo2.png"),
                        width: Globals.dimension * 0.13,
                      ),
                    )),
            const Expanded(
              flex: 3,
              child: SizedBox.shrink(),
            ),
                Expanded(
                    flex: 3,
                    child: Padding(
                      padding: EdgeInsets.all(Globals.dimension * 0.01),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(15),
                        child: Container(
                          color: Globals.color_upload_audio,
                          child: Material(
                            color: Colors.transparent,
                            child: InkWell(
                              onTap: () {
                                controller.pickAudio().then((audio) {
                                  if (audio != null) {
                                    GetX.Get.to(
                                        UploadAudio(audio: audio),
                                        transition: GetX.Transition.downToUp);
                                  }
                                });
                              },
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                    "Translate audio\nfile",
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.w500,
                                      fontSize: Globals.dimension * 0.022,
                                    ),
                                  ),
                                  SizedBox(width: Globals.dimension * 0.02),
                                  Image(
                                    image: const AssetImage(
                                        "assets/upload_audio.png"),
                                    width: Globals.dimension * 0.15,
                                  )
                                ],
                              ),
                            ),
                          ),
                        ),
                      ),
                    )),
              /*Expanded(
                    flex: 3,
                    child: Padding(
                      padding: EdgeInsets.all(Globals.dimension * 0.01),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(15),
                        child: Container(
                          color: Globals.color_live_audio,
                          child: Material(
                            color: Colors.transparent,
                            child: InkWell(
                              onTap: () {},
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                    "Translate live\naudio",
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.w500,
                                      fontSize: Globals.dimension * 0.022,
                                    ),
                                  ),
                                  SizedBox(width: Globals.dimension * 0.02),
                                  Image(
                                    image: const AssetImage(
                                        "assets/live_audio.png"),
                                    width: Globals.dimension * 0.15,
                                  )
                                ],
                              ),
                            ),
                          ),
                        ),
                      ),
                    )),*/
                Expanded(
                    flex: 3,
                    child: Padding(
                      padding: EdgeInsets.all(Globals.dimension * 0.01),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(15),
                        child: Container(
                          color: Globals.color_upload_video,
                          child: Material(
                            color: Colors.transparent,
                            child: InkWell(
                              onTap: () {
                                controller.pickVideo().then((video) {
                                  if (video != null) {
                                    GetX.Get.to(
                                        UploadVideo(video: video),
                                        transition: GetX.Transition.downToUp);
                                  }
                                });
                              },
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                    "Translate video\nfile",
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.w500,
                                      fontSize: Globals.dimension * 0.022,
                                    ),
                                  ),
                                  SizedBox(width: Globals.dimension * 0.02),
                                  Image(
                                    image: const AssetImage(
                                        "assets/upload_video.png"),
                                    width: Globals.dimension * 0.15,
                                  )
                                ],
                              ),
                            ),
                          ),
                        ),
                      ),
                    )),
                /*Expanded(
                    flex: 3,
                    child: Padding(
                      padding: EdgeInsets.all(Globals.dimension * 0.01),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(15),
                        child: Container(
                          color: Globals.color_live_video,
                          child: Material(
                            color: Colors.transparent,
                            child: InkWell(
                              onTap: () {
                                GetX.Get.to(
                                    LiveVideo(),
                                    transition: GetX.Transition.downToUp);
                              },
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                    "Translate live\nvideo",
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.w500,
                                      fontSize: Globals.dimension * 0.022,
                                    ),
                                  ),
                                  SizedBox(width: Globals.dimension * 0.02),
                                  Image(
                                    image: const AssetImage(
                                        "assets/live_video.png"),
                                    width: Globals.dimension * 0.15,
                                  )
                                ],
                              ),
                            ),
                          ),
                        ),
                      ),
                    )),*/
                const Expanded(
                  flex: 3,
                  child: SizedBox.shrink(),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
