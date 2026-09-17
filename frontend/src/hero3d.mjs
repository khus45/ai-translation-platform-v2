import * as THREE from "https://unpkg.com/three@0.160.0/build/three.module.js";

const canvas = document.getElementById("heroScene");

if (canvas) {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
  camera.position.set(0, 0.2, 9.2);

  const renderer = new THREE.WebGLRenderer({
    canvas,
    alpha: true,
    antialias: true,
    powerPreference: "high-performance",
  });

  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const group = new THREE.Group();
  scene.add(group);

  const palette = {
    teal: new THREE.Color("#00a7a0"),
    coral: new THREE.Color("#ff5f7e"),
    gold: new THREE.Color("#ffc857"),
    plum: new THREE.Color("#6f43ff"),
    cyan: new THREE.Color("#2f7dff"),
    ink: new THREE.Color("#0b1020"),
  };

  const ambient = new THREE.AmbientLight("#ffffff", 1.15);
  const key = new THREE.DirectionalLight("#ffffff", 2.8);
  key.position.set(3, 5, 6);
  const rim = new THREE.PointLight("#ff5f7e", 2.1, 9);
  rim.position.set(3.6, 1.8, 2.2);
  const cool = new THREE.PointLight("#55f0d2", 1.8, 8);
  cool.position.set(-1.4, -1.2, 2.8);
  scene.add(ambient, key, rim, cool);

  const glassMaterial = new THREE.MeshPhysicalMaterial({
    color: "#f7f4ed",
    roughness: 0.38,
    metalness: 0.05,
    transmission: 0.22,
    thickness: 0.55,
    transparent: true,
    opacity: 0.78,
  });

  const accentMaterials = [
    new THREE.MeshStandardMaterial({ color: palette.cyan, roughness: 0.42, metalness: 0.24 }),
    new THREE.MeshStandardMaterial({ color: palette.coral, roughness: 0.42, metalness: 0.14 }),
    new THREE.MeshStandardMaterial({ color: palette.gold, roughness: 0.5, metalness: 0.2 }),
    new THREE.MeshStandardMaterial({ color: palette.plum, roughness: 0.44, metalness: 0.18 }),
  ];

  const core = new THREE.Mesh(
    new THREE.TorusKnotGeometry(1.05, 0.26, 120, 18),
    new THREE.MeshStandardMaterial({
      color: palette.cyan,
      roughness: 0.3,
      metalness: 0.36,
    }),
  );
  core.position.set(1.35, 0.12, 0);
  group.add(core);

  const haloGroup = new THREE.Group();
  const ringMaterial = new THREE.MeshStandardMaterial({
    color: palette.gold,
    roughness: 0.25,
    metalness: 0.42,
    transparent: true,
    opacity: 0.72,
  });
  [1.9, 2.28, 2.68].forEach((radius, index) => {
    const ring = new THREE.Mesh(new THREE.TorusGeometry(radius, 0.018, 12, 120), ringMaterial);
    ring.rotation.set(Math.PI / 2 + index * 0.22, index * 0.38, -0.32 + index * 0.18);
    haloGroup.add(ring);
  });
  haloGroup.position.copy(core.position);
  group.add(haloGroup);

  const platform = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.12, 2.55), glassMaterial);
  platform.position.set(1.35, -1.42, -0.55);
  platform.rotation.x = -0.22;
  platform.rotation.z = -0.08;
  group.add(platform);

  const blockGeometry = new THREE.BoxGeometry(1.25, 0.72, 0.18);
  const blocks = [
    [-0.8, 1.1, -0.55, 0],
    [2.95, 0.95, -0.2, 1],
    [-0.4, -0.75, 0.05, 2],
    [3.05, -0.72, 0.18, 3],
    [1.42, 1.82, -0.38, 2],
    [1.1, -1.88, 0.34, 0],
  ].map(([x, y, z, materialIndex]) => {
    const mesh = new THREE.Mesh(blockGeometry, accentMaterials[materialIndex]);
    mesh.position.set(x, y, z);
    mesh.rotation.set(-0.18, 0.28, -0.08);
    group.add(mesh);
    return mesh;
  });

  const nodeGeometry = new THREE.SphereGeometry(0.075, 20, 20);
  const nodeMaterial = new THREE.MeshStandardMaterial({
    color: "#0b1020",
    roughness: 0.36,
    metalness: 0.28,
  });

  const nodePositions = [
    [-1.4, 1.55, -0.3],
    [0.1, 1.82, 0.1],
    [2.02, 1.58, 0.18],
    [3.7, 0.36, -0.12],
    [2.56, -1.62, 0.04],
    [0.52, -1.82, -0.08],
    [-1.34, -0.32, 0.1],
    [4.08, -1.12, 0.16],
    [-0.52, 0.42, 0.54],
  ];

  const nodes = nodePositions.map((position, index) => {
    const node = new THREE.Mesh(nodeGeometry, nodeMaterial);
    node.position.set(...position);
    node.userData.phase = index * 0.62;
    group.add(node);
    return node;
  });

  const linePoints = [];
  nodePositions.forEach((position, index) => {
    const next = nodePositions[(index + 1) % nodePositions.length];
    linePoints.push(new THREE.Vector3(...position), new THREE.Vector3(...next));
  });

  const lineGeometry = new THREE.BufferGeometry().setFromPoints(linePoints);
  const lineMaterial = new THREE.LineBasicMaterial({
    color: "#2f7dff",
    transparent: true,
    opacity: 0.34,
  });
  const network = new THREE.LineSegments(lineGeometry, lineMaterial);
  group.add(network);

  const particlesGeometry = new THREE.BufferGeometry();
  const particleCount = 120;
  const particlePositions = new Float32Array(particleCount * 3);
  for (let i = 0; i < particleCount; i += 1) {
    particlePositions[i * 3] = THREE.MathUtils.randFloatSpread(5.8) + 1.4;
    particlePositions[i * 3 + 1] = THREE.MathUtils.randFloatSpread(3.2);
    particlePositions[i * 3 + 2] = THREE.MathUtils.randFloat(-1.1, 1.2);
  }
  particlesGeometry.setAttribute("position", new THREE.BufferAttribute(particlePositions, 3));
  const particles = new THREE.Points(
    particlesGeometry,
    new THREE.PointsMaterial({
      color: "#55f0d2",
      size: 0.035,
      transparent: true,
      opacity: 0.72,
    }),
  );
  group.add(particles);

  const bars = new THREE.Group();
  const barMaterial = new THREE.MeshStandardMaterial({
    color: palette.ink,
    roughness: 0.52,
    metalness: 0.12,
    transparent: true,
    opacity: 0.62,
  });
  for (let i = 0; i < 18; i += 1) {
    const height = THREE.MathUtils.randFloat(0.16, 0.84);
    const bar = new THREE.Mesh(new THREE.BoxGeometry(0.055, height, 0.055), barMaterial);
    bar.position.set(-1.72 + i * 0.2, -1.5 + height / 2, THREE.MathUtils.randFloat(-0.42, 0.35));
    bar.rotation.y = -0.22;
    bar.userData.phase = i * 0.35;
    bars.add(bar);
  }
  group.add(bars);

  const mouse = { x: 0, y: 0 };
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function resize() {
    const rect = canvas.getBoundingClientRect();
    renderer.setSize(rect.width, rect.height, false);
    camera.aspect = rect.width / rect.height || 1;
    camera.updateProjectionMatrix();
    group.position.x = rect.width < 720 ? 0.85 : 0.05;
    group.position.y = rect.width < 720 ? -0.2 : -0.02;
    group.scale.setScalar(rect.width < 720 ? 0.58 : 0.82);
  }

  window.addEventListener("resize", resize);
  window.addEventListener("pointermove", (event) => {
    mouse.x = (event.clientX / window.innerWidth - 0.5) * 2;
    mouse.y = (event.clientY / window.innerHeight - 0.5) * 2;
  });

  resize();

  function animate(time = 0) {
    const seconds = time * 0.001;
    const drift = prefersReducedMotion ? 0 : seconds;

    core.rotation.x = 0.72 + drift * 0.32;
    core.rotation.y = 0.46 + drift * 0.46;
    haloGroup.rotation.x = Math.sin(drift * 0.42) * 0.18;
    haloGroup.rotation.y = drift * 0.22;
    haloGroup.rotation.z = drift * 0.14;
    platform.rotation.y = -0.18 + Math.sin(drift * 0.7) * 0.04;
    particles.rotation.y = drift * 0.04;
    network.rotation.z = Math.sin(drift * 0.8) * 0.025;

    blocks.forEach((block, index) => {
      block.position.y += Math.sin(drift + index) * 0.0009;
      block.rotation.y = 0.28 + Math.sin(drift * 0.9 + index) * 0.06;
    });

    nodes.forEach((node) => {
      node.position.y += Math.sin(drift * 1.4 + node.userData.phase) * 0.0008;
    });

    bars.children.forEach((bar) => {
      bar.scale.y = 0.76 + Math.sin(drift * 1.8 + bar.userData.phase) * 0.22;
    });

    group.rotation.y += (mouse.x * 0.14 - group.rotation.y) * 0.035;
    group.rotation.x += (-mouse.y * 0.08 - group.rotation.x) * 0.035;

    renderer.render(scene, camera);
    window.requestAnimationFrame(animate);
  }

  animate();
}
