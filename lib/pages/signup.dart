import 'package:flutter/material.dart';

// Signup Link
class SignUpScreen extends StatefulWidget {
  SignUpScreen({Key? key, required this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _SignUpScreenState createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final firstNameController = TextEditingController();
  final lastNameController = TextEditingController();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  final passwordAgainController = TextEditingController();
  bool canChangePage = true;
  bool _isHidden = true;

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
        appBar: AppBar(
          title: Padding(
              padding: EdgeInsets.all(10),
              child: Row(children: [
                Text(
                  "Create Account",
                ),
                Spacer(),
                InkWell(child: Text("Sign In"))
              ])),
          centerTitle: true,
          elevation: 0,
          backgroundColor: Color(0xFF0072ff),
        ),
        backgroundColor: Color(0xFF0072ff),
        body: SafeArea(
          top: true,
          bottom: true,
          child: Padding(
            padding: EdgeInsets.only(top: 10),
            child: Column(
              children: <Widget>[
                Expanded(
                    child: Form(
                  child: Container(
                      padding: EdgeInsets.all(40.0),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.only(
                            topRight: Radius.circular(50),
                            topLeft: Radius.circular(50)),
                      ),
                      child: ListView(
                        children: [
                          Row(children: [
                            Flexible(
                                child: TextFormField(
                              decoration: new InputDecoration(
                                focusedBorder: OutlineInputBorder(
                                    borderSide:
                                        BorderSide(color: Colors.black)),
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
                                labelText: "First name",
                              ),
                            )),
                            SizedBox(
                              width: 15.0,
                            ),
                            Flexible(
                                child: TextFormField(
                              decoration: new InputDecoration(
                                focusedBorder: OutlineInputBorder(
                                    borderSide:
                                        BorderSide(color: Colors.black)),
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
                                labelText: "Last name",
                              ),
                            )),
                          ]),
                          SizedBox(height: 20),
                          TextFormField(
                            controller: passwordController,
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
                          SizedBox(height: 20),
                          TextFormField(
                            controller: passwordController,
                            obscureText: _isHidden,
                            validator: (value) {
                              if (value!.isEmpty) {
                                return 'Please repeat password here';
                              }
                              if (passwordController.text !=
                                  passwordAgainController.text) {
                                return 'Passwords do not match! Please check passwords';
                              }
                              return null;
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
                              labelText: "RepeatPassword",
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
                          SizedBox(height: 20),
                          Row(
                            children: <Widget>[
                              Expanded(
                                  child: ElevatedButton(
                                child: Padding(
                                  padding: EdgeInsets.only(top: 15, bottom: 15),
                                  child: Text("Create an account"),
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
                                onPressed: () => Navigator.pushNamed(
                                    context, '/phoneVerification'),
                              ))
                            ],
                          ),
                          SizedBox(height: 20),
                          Row(
                            children: <Widget>[
                              Expanded(
                                  child: ElevatedButton(
                                child: Padding(
                                  padding: EdgeInsets.only(top: 15, bottom: 15),
                                  child: Text("Continue with Google"),
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
                                onPressed: () {},
                              ))
                            ],
                          ),
                          SizedBox(height: 15.0),
                          Text(
                              "By signing up you agree to our Privacy Policy and Terms",
                              style: TextStyle(fontSize: 15)),
                          SizedBox(height: 15.0),
                          Row(
                            children: [
                              Text("Already have an account?",
                                  style: TextStyle(fontSize: 15)),
                              InkWell(
                                  onTap: () {},
                                  child: Text("Sign in",
                                      style: TextStyle(
                                          fontSize: 15,
                                          decoration:
                                              TextDecoration.underline))),
                            ],
                          ),
                          SizedBox(height: 50.0),
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
