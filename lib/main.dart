import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:workflow/screens/signin.dart';
import 'package:workflow/screens/signup.dart';
import 'package:workflow/screens/task_list.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'Flutter Demo',
        theme: ThemeData(
          // This is the theme of your application.
          //
          // Try running your application with "flutter run". You'll see the
          // application has a blue toolbar. Then, without quitting the app, try
          // changing the primarySwatch below to Colors.green and then invoke
          // "hot reload" (press "r" in the console where you ran "flutter run",
          // or simply save your changes to "hot reload" in a Flutter IDE).
          // Notice that the counter didn't reset back to zero; the application
          // is not restarted.
          primarySwatch: Colors.blue,
        ),
        debugShowCheckedModeBanner: false,
        home: Onboarding(title: 'Flutter Demo Home Page'),
        routes: <String, WidgetBuilder>{
          '/signUp': (BuildContext context) => SignUpScreen(title: "SignUp"),
          '/signIn': (BuildContext context) => SignInScreen(title: "Sign In"),
          '/taskList': (BuildContext context) => TaskListPage(title: "Tasks"),
          '/taskDetail': (BuildContext context) =>
              TaskListPage(title: "Task Detail"),
        });
  }
}

class Onboarding extends StatefulWidget {
  Onboarding({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  _OnboardingState createState() => _OnboardingState();
}

class _OnboardingState extends State<Onboarding> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the Onboarding object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: SafeArea(
        top: true,
        bottom: true,
        child: ListView(
          padding: EdgeInsets.all(30),
          children: [
            ElevatedButton(
                onPressed: () {
                  Navigator.pushReplacementNamed(context, '/signIn');
                },
                child: Text(
                  "Sign In",
                  style: TextStyle(fontSize: 15),
                )),
            SizedBox(height: 20),
            ElevatedButton(
                onPressed: () {
                  Navigator.pushReplacementNamed(context, '/signUp');
                },
                child: Text(
                  "Sign Up",
                  style: TextStyle(fontSize: 15),
                )),
            SizedBox(height: 20),
            ElevatedButton(
                onPressed: () {
                  Navigator.pushReplacementNamed(context, '/taskList');
                },
                child: Text(
                  "Skip",
                  style: TextStyle(fontSize: 15),
                )),
          ],
        ),
      ),
    );
  }
}
