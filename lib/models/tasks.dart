import 'package:workflow/resources/api_client.dart';

class Task {
  final int id;
  final String title;
  final String dateCreated;
  final int order;

  Task(
      {required this.title,
      required this.id,
      required this.dateCreated,
      required this.order});

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
        id: json['id'],
        order: 0,
        title: json['title'],
        dateCreated: json['created']);
  }
}

class TaskResponse {
  int totalResults = 0;
  List<Task> results = [];

  TaskResponse.fromJson(List<dynamic> json) {
    // totalResults = json_list;
    // print("json_list i  $json");
    if (json != null) {
      json.forEach((v) {
        results.add(new Task.fromJson(v));
      });
    }
  }
}

class TaskRepository extends ApiBaseHelper {
  String token = '';

  TaskRepository({
    required this.token,
  });

  Future<List<Task>> fetchTaskList() async {
    final response = await this.get("/tasks/");
    return TaskResponse.fromJson(response).results;
  }

  Future<Task> createTask(String title, String description) async {
    final response = await this
        .post("/tasks/", {"title": title, "description": description});
    return Task.fromJson(response);
  }
}

class TaskForm {}
