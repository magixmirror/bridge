import 'package:flutter/material.dart';
import 'package:bridge/Globals/Globals.dart';

class MyTabBar extends StatelessWidget {
  MyTabBar({Key? key,required List<Tab> this.tabs, required List<Widget> this.tabsContent, double this.height = 0}) : super(key: key);
  List<Tab> tabs;
  List<Widget> tabsContent;
  double height;

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: tabs.length,
      child: Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(
          elevation: 0,
          backgroundColor: Colors.white,
          automaticallyImplyLeading: false,
          bottom: PreferredSize (
            preferredSize: Size.fromHeight(height),
            child: TabBar(
              indicator: const UnderlineTabIndicator(
                //borderRadius: BorderRadius.circular(10),
                borderSide : BorderSide(width: 1.5, color: Globals.color2),
                insets: EdgeInsets.only(bottom: 10),
              ),
              indicatorSize: TabBarIndicatorSize.label,
              tabs: tabs,
            ),
          ),
        ),
        body: TabBarView(
            children: tabsContent
        ),
      ),
    );
  }
}
