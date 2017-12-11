# Todo List Backend

Original Assignment: https://github.com/Cornell-PoBE/A1

## System Configuration

Install requirements.txt
Install SQLite

## Functionality

#### Create a task
`POST /tasks?name={name}&description={description}&tags={tags (comma separated)}&due_date={due date (in unix time)}`

Creates a task given the `URL` params above

#### List all tasks
`GET /tasks`

Get a list of all tasks

#### Get task by ID
`GET /tasks/{id}`

Get a task by its ID

#### Delete a task
`DELETE /tasks/{id}`

Delete a specific task

#### Delete all tasks
`DELETE /tasks/all`

Delete all tasks

#### Search tasks by NAME:

GET /tasks/{name}

Get all tasks with the specific name

#### Search tasks by tag:

GET /tasks/{tag}

Get all tasks with the specific tag.

## Testing 

test.py