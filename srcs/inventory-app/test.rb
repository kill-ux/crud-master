
env = {}
if File.exist?(".env")
  File.read(".env").split("\n").each do |line|
  next if line.strip.empty? || line.start_with?("#")
  key, value = line.strip.split('=', 2)
  env[key] = value.gsub(/^["']|["']$/,'')
  end
end
puts env