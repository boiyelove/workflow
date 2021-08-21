// SignIn Screen
import 'package:flutter/material.dart';

class SignInScreen extends StatefulWidget {
  SignInScreen({Key? key, required this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _SignInScreenState createState() => _SignInScreenState();
}

class _SignInScreenState extends State<SignInScreen> {
  final _passwordController = TextEditingController();
  bool _isHidden = false;

  void _togglePasswordView() {
    setState(() {
      _isHidden = !_isHidden;
    });
  }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
        backgroundColor: Color(0xFF0072ff),
        body: SafeArea(
          top: true,
          bottom: true,
          child: Padding(
            padding: EdgeInsets.only(top: 50),
            child: Column(
              children: <Widget>[
                Expanded(
                    child: Form(
                  child: Container(
                      padding: EdgeInsets.all(50.0),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.only(
                            topRight: Radius.circular(50),
                            topLeft: Radius.circular(50)),
                      ),
                      child: ListView(
                        children: [
                          Align(
                            alignment: Alignment.centerLeft,
                            child: Text(
                              "Welcome",
                              style: TextStyle(
                                  fontWeight: FontWeight.bold, fontSize: 30),
                            ),
                          ),
                          Align(
                            alignment: Alignment.centerLeft,
                            child: Text(
                              "Sign in to continue",
                              style: TextStyle(fontSize: 15),
                            ),
                          ),
                          SizedBox(height: 50.0),
                          TextFormField(
                            decoration: new InputDecoration(
                              focusedBorder: OutlineInputBorder(
                                  borderSide: BorderSide(color: Colors.black)),
                              enabledBorder: OutlineInputBorder(
                                borderSide: BorderSide(color: Colors.grey),
                              ),
                              border: OutlineInputBorder(
                                borderRadius: const BorderRadius.all(
                                  const Radius.circular(10.0),
                                ),
                              ),
                              filled: true,
                              hintStyle: TextStyle(color: Colors.grey[800]),
                              fillColor: Colors.white70,
                              contentPadding: EdgeInsets.all(8),
                              labelText: "Mobile Number or Email",
                            ),
                          ),
                          SizedBox(height: 25.0),
                          TextFormField(
                            controller: _passwordController,
                            obscureText: _isHidden,
                            validator: (value) {
                              if (value!.isNotEmpty && value.length < 8) {
                                return 'Passwords must be 8 characters long';
                              }
                              return 'Please repeat choose a password';
                            },
                            decoration: new InputDecoration(
                              focusedBorder: OutlineInputBorder(
                                  borderSide: BorderSide(color: Colors.black)),
                              enabledBorder: OutlineInputBorder(
                                borderSide: BorderSide(color: Colors.grey),
                              ),
                              border: OutlineInputBorder(
                                borderRadius: const BorderRadius.all(
                                  const Radius.circular(10.0),
                                ),
                              ),
                              filled: true,
                              hintStyle: TextStyle(color: Colors.grey[800]),
                              fillColor: Colors.white70,
                              contentPadding: EdgeInsets.all(8),
                              labelText: "Password",
                              suffix: InkWell(
                                onTap: _togglePasswordView,
                                child: Icon(
                                  _isHidden
                                      ? Icons.visibility
                                      : Icons.visibility_off,
                                ),
                              ),
                            ),
                          ),
                          SizedBox(height: 35.0),
                          Row(
                            children: <Widget>[
                              Expanded(
                                  child: ElevatedButton(
                                child: Padding(
                                  padding: EdgeInsets.only(top: 15, bottom: 15),
                                  child: Text("SIGN IN"),
                                ),
                                style: ElevatedButton.styleFrom(
                                    primary: Color(0xFF0072ff),
                                    shape: new RoundedRectangleBorder(
                                        borderRadius:
                                            BorderRadius.circular(10.0))
                                    // padding: EdgeInsets.symmetric(
                                    //     horizontal: 50, vertical: 20),
                                    // textStyle: TextStyle(
                                    //     fontSize: 30,
                                    //     fontWeight: FontWeight.bold)
                                    ),
                                onPressed: () => Navigator.pushReplacementNamed(
                                    context, '/signIn'),
                              ))
                            ],
                          ),
                          SizedBox(height: 15.0),
                          InkWell(
                            child: Padding(
                              padding: EdgeInsets.all(12.0),
                              child: Text(
                                "Forgot Password ?",
                                textAlign: TextAlign.center,
                                style: TextStyle(fontSize: 15),
                              ),
                            ),
                          ),
                        ],
                      )),
                )),
              ],
            ),
          ),
// This trailing comma makes auto-formatting nicer for build methods.
        ));
  }
}
