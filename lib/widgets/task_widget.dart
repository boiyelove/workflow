import 'package:flutter/material.dart';

class TaskListTile extends StatefulWidget {
  TaskListTile(
      {Key? key,
      required this.id,
      required this.taskName,
      required this.checked})
      : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".
  final int id;
  final String taskName;
  bool checked;

  @override
  _TaskListTileState createState() => _TaskListTileState();
}

class _TaskListTileState extends State<TaskListTile> {
  @override
  Widget build(BuildContext context) {
    return ListTile(
      // tileColor: _items[index].isOdd ? oddItemColor : evenItemColor,
      leading: InkWell(
        onTap: () {
          setState(() {
            widget.checked = !widget.checked;
          });
        },
        child: Container(
          height: 30,
          width: 30,
          child: widget.checked
              ? Icon(
                  Icons.check,
                  color: Colors.white,
                )
              : null,
          decoration: BoxDecoration(
              color: widget.checked ? Colors.blue : Colors.white,
              shape: BoxShape.circle,
              border: widget.checked ? null : Border.all(color: Colors.grey)),
        ),
      ),
      title: Text(
        '${widget.taskName}',
        style: TextStyle(fontSize: 20),
      ),
      trailing: Icon(Icons.arrow_right_alt_sharp),
    );
  }
}
