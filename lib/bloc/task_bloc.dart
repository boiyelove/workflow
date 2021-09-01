// class TaskBloc {
//   late TaskRepository _TaskRepository;
//
//   late StreamController _TaskListController;
//
//   StreamSink<ApiResponse<List<Task>>> get TaskListSink =>
//       _TaskListController.sink;
//
//   Stream<ApiResponse<List<Task>>> get TaskListStream =>
//       _TaskListController.stream;
//
//   TaskBloc() {
//     _TaskListController = StreamController<ApiResponse<List<Task>>>();
//     _TaskRepository = TaskRepository();
//     fetchTaskList();
//   }
//
//   fetchTaskList() async {
//     TaskListSink.add(ApiResponse.loading('Fetching Popular Tasks'));
//     try {
//       List<Task> Tasks = await _TaskRepository.fetchTaskList();
//       TaskListSink.add(ApiResponse.completed(Tasks));
//     } catch (e) {
//       TaskListSink.add(ApiResponse.error(e.toString()));
//       print(e);
//     }
//   }
//
//   dispose() {
//     _TaskListController?.close();
//   }
// }
