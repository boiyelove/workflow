import 'package:flutter/material.dart';
import 'package:workflow/models/tasks.dart';

class SimpleTaskBottomSheet extends StatefulWidget {
  SimpleTaskBottomSheet({Key? key, required this.taskRepository})
      : super(key: key);

  TaskRepository taskRepository;
  @override
  _SimpleTaskBottomSheetState createState() => _SimpleTaskBottomSheetState();
}

class _SimpleTaskBottomSheetState extends State<SimpleTaskBottomSheet> {
  var selectedDate;
  var selectedTime;
  bool showDescriptionField = false;
  List assignees = [];
  TextEditingController _titleController = TextEditingController();
  TextEditingController _descriptionController = TextEditingController();

  _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(), // Refer step 1
      firstDate: DateTime(2000),
      lastDate: DateTime(2025),
    );
    if (picked != null && picked != selectedDate)
      setState(() {
        selectedDate = picked;
      });
    print("launched the datepicker");
  }

  Future<Null> _selectTime(BuildContext context) async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: TimeOfDay(hour: 7, minute: 00),
    );
    if (picked != null)
      setState(() {
        selectedTime = picked;
      });
  }

  _showDescription() {
    setState(() {
      print("show description is $showDescriptionField");
      showDescriptionField = !showDescriptionField;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 15, bottom: 15, left: 30, right: 30),
      child: Container(
        padding:
            EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            TextField(
              controller: _titleController,
              style:
                  TextStyle(fontSize: 20.0, height: 1.3, color: Colors.black),
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
              maintainState: true,
              child: AnimatedOpacity(
                  opacity: showDescriptionField ? 1.0 : 0.0,
                  duration: const Duration(milliseconds: 500),
                  child: TextField(
                    controller: _descriptionController,
                    keyboardType: TextInputType.multiline,
                    style: TextStyle(
                        fontSize: 15.0, height: 1.3, color: Colors.black),
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
                  )),
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
                      color: showDescriptionField ? Colors.blue : Colors.grey,
                    ),
                    onPressed: () => _showDescription(),
                  ),
                  IconButton(
                    icon: Icon(
                      Icons.event,
                      color: (selectedDate != null) ? Colors.blue : Colors.grey,
                    ),
                    onPressed: () => _selectDate(context),
                  ),
                  IconButton(
                    icon: Icon(
                      Icons.schedule_outlined,
                      color: (selectedTime != null) ? Colors.blue : Colors.grey,
                    ),
                    onPressed: () => _selectTime(context),
                  ),
                  IconButton(
                    icon: Icon(
                      Icons.group_add,
                      color: assignees.isNotEmpty ? Colors.blue : Colors.grey,
                    ),
                    onPressed: () {},
                  ),
                  Spacer(),
                  TextButton(
                    style: TextButton.styleFrom(
                      textStyle: TextStyle(
                        fontSize: 18,
                        color: Colors.blue,
                      ),
                    ),
                    onPressed: () async {
                      TaskRepository task_repo = widget.taskRepository;
                      Task task = await task_repo.createTask(
                          _titleController.text, _descriptionController.text);
                      Navigator.pop(context, task);
                    },
                    child: Text("Save"),
                  )
                ],
              ),
            ),
            SizedBox(height: 10),
          ],
        ),
      ),
    );
  }
}
