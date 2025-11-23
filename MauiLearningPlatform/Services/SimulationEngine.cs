using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text.RegularExpressions;

namespace MauiLearningPlatform.Services
{
    public class SimulationEngine
    {
        // A simple registry of "compiled" types
        private Dictionary<string, SimulatedType> _types = new();
        private Dictionary<string, object> _instances = new();

        public void Compile(List<VirtualFile> files)
        {
            _types.Clear();
            _instances.Clear();

            // 1. Scan all C# files
            foreach (var file in files.Where(f => f.Type == "csharp"))
            {
                ParseFile(file.Content);
            }

            // 2. Register Services (Simple DI)
            // Find all classes that implement an interface
            foreach (var type in _types.Values.Where(t => !t.IsInterface))
            {
                foreach (var iface in type.Interfaces)
                {
                    // Singleton registration simulation
                    if (!_instances.ContainsKey(iface))
                    {
                        var instance = CreateInstance(type.Name);
                        _instances[iface] = instance;
                    }
                }
            }
        }

        public object GetViewModel(string viewModelName)
        {
            return CreateInstance(viewModelName);
        }

        private void ParseFile(string code)
        {
            // Regex to find class/interface definitions
            // public partial class MainViewModel : ObservableObject
            // Handles public [partial/abstract/sealed] class/interface Name : Base
            var classRegex = new Regex(@"public\s+(?:partial\s+|abstract\s+|sealed\s+)*(class|interface)\s+(\w+)(?:\s*:\s*([\w\s,]+))?");
            var matches = classRegex.Matches(code);

            foreach (Match match in matches)
            {
                var kind = match.Groups[1].Value; // class or interface
                var name = match.Groups[2].Value;
                var inherits = match.Groups[3].Value;

                var type = new SimulatedType
                {
                    Name = name,
                    IsInterface = kind == "interface",
                    Code = code // Store full code for method parsing later
                };

                if (!string.IsNullOrWhiteSpace(inherits))
                {
                    var interfaces = inherits.Split(',').Select(i => i.Trim()).ToList();
                    type.Interfaces.AddRange(interfaces);
                }

                _types[name] = type;
            }
        }

        private object CreateInstance(string typeName)
        {
            if (!_types.ContainsKey(typeName)) return null;

            var type = _types[typeName];
            var instance = new SimulatedObject(type.Name);

            // 1. Constructor Injection
            // Find constructor: public MainViewModel(INoteRepository repository)
            var ctorRegex = new Regex($@"public\s+{type.Name}\s*\(([^)]*)\)");
            var ctorMatch = ctorRegex.Match(type.Code);

            if (ctorMatch.Success)
            {
                var args = ctorMatch.Groups[1].Value;
                if (!string.IsNullOrWhiteSpace(args))
                {
                    var paramParts = args.Split(',');
                    foreach (var param in paramParts)
                    {
                        var p = param.Trim().Split(' '); // INoteRepository repository
                        var paramType = p[0];
                        var paramName = p[1];

                        if (_instances.ContainsKey(paramType))
                        {
                            instance.Fields[paramName] = _instances[paramType];
                            instance.Fields["_" + paramName] = _instances[paramType]; // Common convention
                        }
                    }
                }
            }

            // 2. Parse Methods and Properties
            ParseMembers(instance, type.Code);

            // 3. Run Constructor Logic (Simplified)
            // We just look for "Refresh();" or similar calls inside the constructor body
            // This is very basic simulation
            if (type.Code.Contains("Refresh();"))
            {
                instance.ExecuteMethod("Refresh");
            }

            return instance;
        }

        private void ParseMembers(SimulatedObject instance, string code)
        {
            // [ObservableProperty] private string name;
            var propRegex = new Regex(@"\[ObservableProperty\]\s*private\s+\w+\s+(\w+);");
            foreach (Match m in propRegex.Matches(code))
            {
                var fieldName = m.Groups[1].Value;
                // Capitalize for property: name -> Name
                var propName = char.ToUpper(fieldName[0]) + fieldName.Substring(1);
                instance.Set(propName, ""); 
            }

            // [RelayCommand] private void AddNote()
            var cmdRegex = new Regex(@"\[RelayCommand\]\s*private\s+void\s+(\w+)\(\)");
            foreach (Match m in cmdRegex.Matches(code))
            {
                var methodName = m.Groups[1].Value;
                var commandName = methodName + "Command";
                
                instance.RegisterCommand(commandName, () => 
                {
                    instance.ExecuteMethod(methodName);
                });
            }

            // Parse methods bodies (EXTREMELY BASIC)
            // We are just extracting the body to execute later via simple interpretation
            var methodBodyRegex = new Regex(@"private\s+void\s+(\w+)\(\)\s*\{([\s\S]*?)\}");
            foreach (Match m in methodBodyRegex.Matches(code))
            {
                var name = m.Groups[1].Value;
                var body = m.Groups[2].Value;
                instance.DefineMethod(name, body);
            }
        }
    }

    public class SimulatedType
    {
        public string Name { get; set; }
        public bool IsInterface { get; set; }
        public List<string> Interfaces { get; set; } = new();
        public string Code { get; set; }
    }

    public class SimulatedObject : System.ComponentModel.INotifyPropertyChanged
    {
        public string TypeName { get; }
        public Dictionary<string, object> Fields { get; } = new();
        private Dictionary<string, object> _properties = new();
        private Dictionary<string, Action> _commands = new();
        private Dictionary<string, string> _methods = new();

        public event System.ComponentModel.PropertyChangedEventHandler PropertyChanged;

        public SimulatedObject(string typeName)
        {
            TypeName = typeName;
        }

        public object Get(string name) => _properties.ContainsKey(name) ? _properties[name] : null;
        
        public void Set(string name, object value)
        {
            _properties[name] = value;
            PropertyChanged?.Invoke(this, new System.ComponentModel.PropertyChangedEventArgs(name));
        }

        public void RegisterCommand(string name, Action action) => _commands[name] = action;
        
        public void ExecuteCommand(string name) 
        {
            if (_commands.ContainsKey(name)) _commands[name]();
        }

        public void DefineMethod(string name, string body) => _methods[name] = body;

        public void ExecuteMethod(string name)
        {
            if (!_methods.ContainsKey(name)) return;
            var body = _methods[name];

            // SUPER BASIC INTERPRETER
            // 1. _repository.AddNote(NewNoteText);
            if (body.Contains("_repository.AddNote(NewNoteText)"))
            {
                var repo = Fields.Values.FirstOrDefault(v => v is SimulatedObject s && s.TypeName == "NoteRepository") as SimulatedObject;
                var note = Get("NewNoteText")?.ToString();
                if (repo != null && !string.IsNullOrEmpty(note))
                {
                    repo.ExecuteMethod("AddNote", note);
                }
            }
            
            // 2. Refresh();
            if (body.Contains("Refresh();"))
            {
                ExecuteMethod("Refresh");
            }

            // 3. Notes.Clear();
            if (body.Contains("Notes.Clear();"))
            {
                var notes = Get("Notes") as System.Collections.ObjectModel.ObservableCollection<string>;
                notes?.Clear();
            }

            // 4. foreach (var note in _repository.GetNotes())
            if (body.Contains("_repository.GetNotes()"))
            {
                var repo = Fields.Values.FirstOrDefault(v => v is SimulatedObject s && s.TypeName == "NoteRepository") as SimulatedObject;
                if (repo != null)
                {
                    var notes = repo.Get("NotesList") as List<string>; // Internal storage of repo
                    var vmNotes = Get("Notes") as System.Collections.ObjectModel.ObservableCollection<string>;
                    
                    if (notes != null && vmNotes != null)
                    {
                        foreach (var n in notes) vmNotes.Add(n);
                    }
                }
            }
        }

        // Overload for repo methods
        public void ExecuteMethod(string name, object arg)
        {
            if (TypeName == "NoteRepository" && name == "AddNote")
            {
                var list = Get("NotesList") as List<string>;
                if (list == null)
                {
                    list = new List<string>();
                    Set("NotesList", list);
                }
                list.Add(arg.ToString());
            }
        }
    }
}
