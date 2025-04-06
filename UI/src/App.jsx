import React, { useState } from "react";
import { Provider } from "@/components/ui/provider"
import {
  Box,
  Button,
  Table,
  Drawer,
  CloseButton,
  Portal,
  DataList
} from "@chakra-ui/react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

// Dummy data for table
const locations = [
  { id: 1, name: "Location A", lat: 51.505, lng: -0.09 },
  { id: 2, name: "Location B", lat: 51.515, lng: -0.1 },
  { id: 3, name: "Location C", lat: 51.525, lng: -0.11 }
];

function App() {
  const [selectedLocation, setSelectedLocation] = useState(null);

  const [isOpen, setIsOpen] = useState(false);

  React.useEffect(() => {
    if (selectedLocation) {
      setIsOpen(true);
    }
  }, [selectedLocation]);

  return (
    <Provider>
      <Box display="flex" height="100vh" p={4}>
        {/* Table Section */}
        <Box flex="1" overflowY="auto" pr={4}>
          <Table.ScrollArea borderWidth="1px" rounded="md" height="160px">
            <Table.Root size="sm" stickyHeader>
              <Table.Header>
                <Table.Row bg="bg.subtle">
                  <Table.ColumnHeader>ID</Table.ColumnHeader>
                  <Table.ColumnHeader>Name</Table.ColumnHeader>
                  <Table.ColumnHeader>Lat</Table.ColumnHeader>
                  <Table.ColumnHeader>Lng</Table.ColumnHeader>
                </Table.Row>
              </Table.Header>
              <Table.Body>
                {locations.map((item) => (
                  <Table.Row
                    key={item.id}
                    onClick={() => setSelectedLocation(item)}
                    cursor="pointer"
                  >
                    <Table.Cell>{item.id}</Table.Cell>
                    <Table.Cell>{item.name}</Table.Cell>
                    <Table.Cell>{item.lat}</Table.Cell>
                    <Table.Cell>{item.lng}</Table.Cell>
                  </Table.Row>
                ))}
              </Table.Body>
            </Table.Root>
          </Table.ScrollArea>
        </Box>

        {/* Map Section */}
        <Box flex="2" position="relative">
          <MapContainer
            center={[51.505, -0.09]}
            zoom={13}
            style={{ height: "100%", width: "100%" }}
          >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {locations.map((loc) => (
              <Marker
                key={loc.id}
                position={[loc.lat, loc.lng]}
                eventHandlers={{
                  click: () => setSelectedLocation(loc),
                }}
              >
                <Popup>{loc.name}</Popup>
              </Marker>
            ))}
          </MapContainer>
        </Box>

        <Drawer.Root open={isOpen} onOpenChange={(e) => {
          setIsOpen(e.open);
          if (!e.open) setSelectedLocation(null);
        }}>
          <Portal>
            <Drawer.Backdrop />
            <Drawer.Positioner padding="4">
              <Drawer.Content rounded="md">
                <Drawer.Header>
                  <Drawer.Title>{selectedLocation?.name}</Drawer.Title>
                </Drawer.Header>
                <Drawer.Body>
                  {selectedLocation && (
                  <DataList.Root>
                    <DataList.Item>
                      <DataList.ItemLabel>ID</DataList.ItemLabel>
                      <DataList.ItemValue>{selectedLocation.id}</DataList.ItemValue>
                    </DataList.Item><DataList.Item>
                      <DataList.ItemLabel>Name</DataList.ItemLabel>
                      <DataList.ItemValue>{selectedLocation.name}</DataList.ItemValue>
                    </DataList.Item><DataList.Item>
                      <DataList.ItemLabel>Lat</DataList.ItemLabel>
                      <DataList.ItemValue>{selectedLocation.lat}</DataList.ItemValue>
                    </DataList.Item><DataList.Item>
                      <DataList.ItemLabel>Lng</DataList.ItemLabel>
                      <DataList.ItemValue>{selectedLocation.lng}</DataList.ItemValue>
                    </DataList.Item>
                  </DataList.Root>
                  )}
                </Drawer.Body>
                <Drawer.CloseTrigger asChild>
                  <CloseButton size="sm" />
                </Drawer.CloseTrigger>
              </Drawer.Content>
            </Drawer.Positioner>
          </Portal>
        </Drawer.Root>
      </Box>
    </Provider>
  );
}

export default App;