import { Task } from "../types";
import { format } from "date-fns";
import axios from "axios";

interface TaskListProps {
  tasks: Task[];
  onTaskUpdate: () => void;
}

export default function TaskList({ tasks, onTaskUpdate }: TaskListProps) {
  const toggleTaskStatus = async (task: Task) => {
    try {
      await axios.put(`http://localhost:8000/api/v1/tasks/${task.id}`, {
        completed: !task.completed,
      });
      onTaskUpdate();
    } catch (error) {
      console.error("Error updating task:", error);
    }
  };

  return (
    <ul className="divide-y divide-gray-200">
      {tasks.map((task) => (
        <li key={task.id} className="py-4">
          <div className="flex items-center space-x-4">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => toggleTaskStatus(task)}
              className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <div className="flex-1 min-w-0">
              <p
                className={`text-sm font-medium text-gray-900 ${
                  task.completed ? "line-through" : ""
                }`}
              >
                {task.title}
              </p>
              {task.description && (
                <p className="text-sm text-gray-500">{task.description}</p>
              )}
              {task.due_date && (
                <p className="text-xs text-gray-400">
                  Due: {format(new Date(task.due_date), "PPP")}
                </p>
              )}
            </div>
          </div>
        </li>
      ))}
    </ul>
  );
}
