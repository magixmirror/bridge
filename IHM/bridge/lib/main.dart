import 'package:flutter/cupertino.dart';
import 'package:get/get.dart' as GetX;
import "package:bridge/Pages/Loading.dart";
import "package:bridge/Pages/Home.dart";

void main() async{
  runApp(GetX.GetMaterialApp(
      initialRoute: '/Loading',
      getPages: [
        GetX.GetPage(name: '/Loading', page: () => Loading()),
        GetX.GetPage(name: '/Home', page: () => Home()),
      ],
      debugShowCheckedModeBanner: false));
}
