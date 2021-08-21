import 'package:flutter/material.dart';

class TaskDetailPage extends StatefulWidget {
  TaskDetailPage({Key? key, required this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _TaskDetailPageState createState() => _TaskDetailPageState();
}

class _TaskDetailPageState extends State<TaskDetailPage> {
  @override
  Widget build(BuildContext context) {
    final List<int> _items = List<int>.generate(50, (int index) => index);
    var showDescriptionField = true;

    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the TaskListPage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: SafeArea(
        top: true,
        bottom: true,
        child: ReorderableListView(
          padding: const EdgeInsets.symmetric(horizontal: 10),
          children: <Widget>[
            for (int index = 0; index < _items.length; index++)
              Padding(
                key: Key('$index'),
                padding: EdgeInsets.only(top: 10, bottom: 10),
                child: ListTile(
                  // tileColor: _items[index].isOdd ? oddItemColor : evenItemColor,

                  leading: InkWell(
                    onTap: () {},
                    child: Container(
                      height: 30,
                      width: 30,
                      decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          border: Border.all(color: Colors.black)),
                    ),
                  ),
                  title: Text(
                    'Item ${_items[index]}',
                    style: TextStyle(fontSize: 20),
                  ),
                  trailing: Icon(Icons.reorder_outlined),
                ),
              ),
          ],
          onReorder: (int oldIndex, int newIndex) {
            setState(() {
              if (oldIndex < newIndex) {
                newIndex -= 1;
              }
              final int item = _items.removeAt(oldIndex);
              _items.insert(newIndex, item);
            });
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          showModalBottomSheet(
              shape: RoundedRectangleBorder(
                  borderRadius:
                      BorderRadius.vertical(top: Radius.circular(10.0))),
              context: context,
              isScrollControlled: true,
              builder: (context) => Padding(
                    padding: const EdgeInsets.only(
                        top: 15, bottom: 15, left: 30, right: 30),
                    child: Container(
                      padding: EdgeInsets.only(
                          bottom: MediaQuery.of(context).viewInsets.bottom),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisSize: MainAxisSize.min,
                        children: <Widget>[
                          TextField(
                            style: TextStyle(
                                fontSize: 20.0,
                                height: 1.3,
                                color: Colors.black),
                            decoration: InputDecoration(
                              hintText: 'New Task',
                              border: InputBorder.none,
                              focusedBorder: InputBorder.none,
                              enabledBorder: InputBorder.none,
                              errorBorder: InputBorder.none,
                              disabledBorder: InputBorder.none,
                              contentPadding: EdgeInsets.all(5),
                            ),
                            autofocus: true,
                          ),
                          Visibility(
                            child: TextField(
                              keyboardType: TextInputType.multiline,
                              style: TextStyle(
                                  fontSize: 15.0,
                                  height: 1.3,
                                  color: Colors.black),
                              decoration: InputDecoration(
                                hintText: 'Add Description',
                                border: InputBorder.none,
                                focusedBorder: InputBorder.none,
                                enabledBorder: InputBorder.none,
                                errorBorder: InputBorder.none,
                                disabledBorder: InputBorder.none,
                                contentPadding: EdgeInsets.all(5),
                              ),
                              autofocus: false,
                              minLines: 1,
                              maxLines: 20,
                              maxLength: 1000,
                            ),
                            visible: showDescriptionField,
                          ),
                          Visibility(
                            child: SizedBox(height: 10),
                            visible: showDescriptionField,
                          ),
                          Container(
                            padding: EdgeInsets.only(top: 10.0),
                            decoration: BoxDecoration(
                                border: Border(
                                    top: BorderSide(
                              width: 0.2,
                              color: Colors.grey,
                            ))),
                            child: Row(
                              children: [
                                IconButton(
                                  icon: Icon(
                                    Icons.notes_outlined,
                                    color: showDescriptionField
                                        ? Colors.blue
                                        : Colors.grey,
                                  ),
                                  onPressed: () {
                                    setState(() {
                                      showDescriptionField =
                                          !showDescriptionField;
                                    });
                                  },
                                ),
                                IconButton(
                                  icon: Icon(
                                    Icons.event,
                                    color: showDescriptionField
                                        ? Colors.blue
                                        : Colors.grey,
                                  ),
                                  onPressed: () {
                                    setState(() {
                                      showDescriptionField =
                                          !showDescriptionField;
                                    });
                                  },
                                ),
                                IconButton(
                                  icon: Icon(
                                    Icons.schedule_outlined,
                                    color: showDescriptionField
                                        ? Colors.blue
                                        : Colors.grey,
                                  ),
                                  onPressed: () {
                                    setState(() {
                                      showDescriptionField =
                                          !showDescriptionField;
                                    });
                                  },
                                ),
                                IconButton(
                                  icon: Icon(
                                    Icons.group_add,
                                    color: showDescriptionField
                                        ? Colors.blue
                                        : Colors.grey,
                                  ),
                                  onPressed: () {
                                    setState(() {
                                      showDescriptionField =
                                          !showDescriptionField;
                                    });
                                  },
                                ),
                                Spacer(),
                                TextButton(
                                  style: TextButton.styleFrom(
                                    textStyle: TextStyle(
                                      fontSize: 18,
                                      color: Colors.blue,
                                    ),
                                  ),
                                  onPressed: () {},
                                  child: Text("Save"),
                                )
                              ],
                            ),
                          ),
                          SizedBox(height: 10),
                        ],
                      ),
                    ),
                  ));
        },
        tooltip: 'Increment',
        child: Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}