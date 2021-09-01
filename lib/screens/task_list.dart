import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:workflow/models/tasks.dart';
import 'package:workflow/widgets/simpleTaskBottomSheet_widget.dart';
import 'package:workflow/widgets/task_widget.dart';

class TaskListPage extends StatefulWidget {
  TaskListPage({Key? key, required this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _TaskListPageState createState() => _TaskListPageState();
}

class _TaskListPageState extends State<TaskListPage> {
  late Future<List<Task>> taskList;
  TaskRepository task_repo =
      TaskRepository(token: "50e811c11249109159f5b42e9633a961086d0430");

  @override
  void initState() {
    // TODO: implement initState
    taskList = task_repo.fetchTaskList();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the TaskListPage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: SafeArea(
        top: true,
        bottom: true,
        child: FutureBuilder<List<Task>>(
          future: taskList, // async work
          builder: (BuildContext context, AsyncSnapshot<List> snapshot) {
            switch (snapshot.connectionState) {
              case ConnectionState.waiting:
                return Center(child: CircularProgressIndicator());
              default:
                if (snapshot.hasError)
                  return Center(child: Text('${snapshot.error}'));
                else if (snapshot.hasData) {
                  var _items = snapshot.data!;
                  return ReorderableListView.builder(
                    padding: const EdgeInsets.symmetric(horizontal: 10),
                    itemCount: _items.length,
                    itemBuilder: (context, index) {
                      Task task = _items[index];
                      return Dismissible(
                          key: ValueKey<int>(task.id),
                          onDismissed: (DismissDirection direction) {
                            if (direction == DismissDirection.startToEnd) {
                            } else if (direction ==
                                DismissDirection.startToEnd) {}
                            setState(() {
                              _items.removeAt(index);
                            });

                            ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                                content: Text('${task.title} dismissed')));
                          },
                          background: Container(color: Colors.blue),
                          child: Padding(
                            padding: EdgeInsets.only(top: 10, bottom: 10),
                            child: TaskListTile(
                                taskName: "${task.title}",
                                id: task.id,
                                checked: false),
                          ));
                    },
                    onReorder: (int oldIndex, int newIndex) {
                      setState(() {
                        if (oldIndex < newIndex) {
                          newIndex -= 1;
                        }
                        var item = _items.removeAt(oldIndex);
                        _items.insert(newIndex, item);
                      });
                    },
                  );
                }
                return Center(child: Text("Request finished"));
            }
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          Task task = await showModalBottomSheet(
              shape: RoundedRectangleBorder(
                  borderRadius:
                      BorderRadius.vertical(top: Radius.circular(10.0))),
              context: context,
              isScrollControlled: true,
              builder: (BuildContext context) =>
                  SimpleTaskBottomSheet(taskRepository: task_repo));
          print('Task is $task');
          await taskList.Insert(0, task);
        },
        child: Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
